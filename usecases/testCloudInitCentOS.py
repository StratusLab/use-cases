import unittest
import os, os.path

from usecases.TestUtils import *

class testCloudInitCentOS(unittest.TestCase):

    vm_image_info = getVmImageInfo()
    marketplaceId = vm_image_info['centos']['id']

    ssh_key_path = os.path.join(os.path.expanduser('~'), '.ssh', 'id_rsa.pub')

    script_path = None

    # contents MUST NOT start with a newline!
    SCRIPT_CONTENTS = '''#!/bin/bash -x

yum install -y httpd 

cat > /var/www/html/test.txt <<EOF
SUCCESSFUL TEST
EOF

chkconfig httpd on 

service httpd start
'''

    def _createScript(self):
        _, path = tempfile.mkstemp()
        with open(path, 'wb') as f:
            f.write(self.SCRIPT_CONTENTS)
        return path

    def _cloudinit_arg(self, script_path):
        cloudinit_args = ['ssh,%s' % self.ssh_key_path,
                          'none,%s' % script_path]
        return '#'.join(cloudinit_args)

    def setUp(self):
        self.script_path = self._createScript()
        cloudinit_arg = self._cloudinit_arg(self.script_path)

        self.vm_id, self.vm_ip = stratusRunInstance(self.marketplaceId,
                                                    options=['--cloud-init',
                                                             cloudinit_arg])

    def tearDown(self):
        if (self.script_path):
            os.remove(self.script_path)

        stratusKillInstance(self.vm_id)

    def test_usecase(self):
        waitVmRunningOrTimeout(self.vm_id, timeout=(5*60))
        sshConnectionOrTimeout(self.vm_ip, timeout=(5*60))

        url = 'http://%s/test.txt' % self.vm_ip
        print url
        resp, content = getUrlOrTimeout(url)

        self.assertEqual("SUCCESSFUL TEST\n", content)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testCloudInitCentOS)
