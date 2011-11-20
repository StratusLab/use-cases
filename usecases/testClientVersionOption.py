import unittest
import os, os.path

from usecases.TestUtils import *

class testClientVersionOption(unittest.TestCase):

    def _execute_help_option(self, file):
        # FIXME: This exception should not be made.
        if (file != 'stratus-ovf'):
            print which(file)
            execute([file, "--version"])

    def test_client_version_option(self):
        for f in os.listdir(stratuslabBinDir()):
            self._execute_help_option(f)

suite = unittest.TestLoader().loadTestsFromTestCase(testClientVersionOption)
unittest.TextTestRunner(verbosity=2).run(suite)
