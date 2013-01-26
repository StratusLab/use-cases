import unittest
from base64 import b64decode, b64encode
from contextlib import closing
import StringIO
from gzip import GzipFile
import tempfile
import os, os.path

from usecases.TestUtils import *

class testPrepareContext(unittest.TestCase):

    CONTEXT_FILE = 'cloud-init.txt'

    # newline will always be added to ssh key; ensure content has one
    SSH_CONTENT = "ssh\n"
    SCRIPT_CONTENT = 'script'

    vm_image_info = getVmImageInfo()

    ssh_path = None
    script_path = None

    def _tmpfile(self, contents):
        _, path = tempfile.mkstemp()
        with open(path, 'wb') as f:
            f.write(contents)
        return path

    def _map_from_context(self):
        result = {}
        with open(self.CONTEXT_FILE) as f:
            for line in f:
                line = line.rstrip("\n\r")
                if line:
                    key, value = line.split('=', 1)
                    result[key] = value
        return result

    def _decode_ssh(self, b64value):
        return b64decode(b64value.strip())

    def _decode_script(self, b64value):
        gzipped_data = b64decode(b64value.strip())
        with closing(StringIO.StringIO(gzipped_data)) as buffer:
            with closing(GzipFile('', 'rb', 9, buffer)) as f:
                return f.read()

    def setUp(self):
        self.ssh_path = self._tmpfile(self.SSH_CONTENT)
        self.script_path = self._tmpfile(self.SCRIPT_CONTENT)

    def tearDown(self):
        if self.ssh_path:
            os.remove(self.ssh_path)
        if self.script_path:
            os.remove(self.script_path)
        if os.path.exists(self.CONTEXT_FILE):
            os.remove(self.CONTEXT_FILE)

    def test_usecase(self):
        args = ['ssh,%s' % self.ssh_path,
                'none,%s' % self.script_path]
        print args
        stratusPrepareContext(args)

        self.assertTrue(os.path.exists(self.CONTEXT_FILE))

        context = self._map_from_context()

        self.assertTrue(context['CONTEXT_METHOD'])
        self.assertTrue(context['CLOUD_INIT_AUTHORIZED_KEYS'])
        self.assertTrue(context['CLOUD_INIT_USER_DATA'])

        self.assertEqual(context['CONTEXT_METHOD'], 'cloud-init')
        self.assertEqual(self._decode_ssh(context['CLOUD_INIT_AUTHORIZED_KEYS']), self.SSH_CONTENT)
        self.assertEqual(self._decode_script(context['CLOUD_INIT_USER_DATA']), self.SCRIPT_CONTENT)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testPrepareContext)
