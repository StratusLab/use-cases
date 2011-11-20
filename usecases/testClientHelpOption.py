import unittest

import usecases.TestUtils

class testClientHelpOption(unittest.TestCase):

    def setUp(self):
        print "setUp"

    def tearDown(self):
        print "tearDown"

    def test_something(self):
        print "test_something"

suite = unittest.TestLoader().loadTestsFromTestCase(testClientHelpOption)
unittest.TextTestRunner(verbosity=2).run(suite)
