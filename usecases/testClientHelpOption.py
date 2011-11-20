import unittest
import os, os.path

from usecases.TestUtils import *

class testClientHelpOption(unittest.TestCase):

    def _execute_help_option(self, file):
        print which(file)

    def setUp(self):
        print "setUp"

    def tearDown(self):
        print "tearDown"

    def test_something(self):
        dir = '/Users/loomis/stratuslab/bin'
        for f in os.listdir(dir):
            self._execute_help_option(f)

suite = unittest.TestLoader().loadTestsFromTestCase(testClientHelpOption)
unittest.TextTestRunner(verbosity=2).run(suite)
