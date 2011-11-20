import unittest
import os, os.path

from usecases.TestUtils import *

class testClientVersionOption(unittest.TestCase):

    def _execute_version_option(self, cmd):
        # FIXME: This exception should not be made.
        if (cmd != 'stratus-ovf'):
            execute([cmd, "--version"])

    def test_client_version_option(self):
        for cmd in os.listdir(stratuslabBinDir()):
            if (cmd.startswith("stratus-")):
                self._execute_version_option(cmd)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(testClientHelpOption)
