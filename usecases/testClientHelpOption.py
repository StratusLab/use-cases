import unittest
import os, os.path

from usecases.TestUtils import *

class testClientHelpOption(unittest.TestCase):

    def _execute_help_option(self, file):
        # FIXME: This exception should not be made.
        if (file != 'stratus-ovf'):
            print which(file)
            execute([file, "--help"])

    def test_client_help_option(self):
        for f in os.listdir(stratuslabBinDir()):
            self._execute_help_option(f)

suite = unittest.TestLoader().loadTestsFromTestCase(testClientHelpOption)
unittest.TextTestRunner().run(suite)
