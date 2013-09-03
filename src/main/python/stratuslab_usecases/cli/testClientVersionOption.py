import unittest
import os, os.path

from stratuslab_usecases.cli.TestUtils import *

class testClientVersionOption(unittest.TestCase):

    def _execute_version_option(self, cmd):
        execute([cmd, "--version"])

    def test_usecase(self):
        for cmd in os.listdir(stratuslabBinDir()):
            if (cmd.startswith("stratus-")):
                self._execute_version_option(cmd)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testClientVersionOption)
