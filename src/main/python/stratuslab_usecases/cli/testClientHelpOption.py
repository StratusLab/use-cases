import unittest
import os, os.path

from stratuslab_usecases.cli.TestUtils import *

class testClientHelpOption(unittest.TestCase):

    def _execute_help_option(self, cmd):
        execute([cmd, "--help"])

    def test_usecase(self):
        for cmd in os.listdir(stratuslabBinDir()):
            if (cmd.startswith("stratus-")):
                self._execute_help_option(cmd)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testClientHelpOption)
