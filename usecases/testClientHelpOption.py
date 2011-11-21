import unittest
import os, os.path

from usecases.TestUtils import *

class testClientHelpOption(unittest.TestCase):

    def _execute_help_option(self, cmd):
        # FIXME: This exception should not be made.
        if (cmd != 'stratus-ovf'):
            execute([cmd, "--help"])

    def test_client_help_option(self):
        for cmd in os.listdir(stratuslabBinDir()):
            if (cmd.startswith("stratus-")):
                self._execute_help_option(cmd)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testClientHelpOption)
