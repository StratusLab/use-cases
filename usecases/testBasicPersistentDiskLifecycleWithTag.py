import unittest
import os, os.path

from usecases.TestUtils import *

class testBasicPersistentDiskLifecycle(unittest.TestCase):

    diskSize = 1 # in gigabytes
    tag = '"tag \' with } very $ dangerous \\" characters"'

    def setUp(self):
        self.uuid = stratusCreateVolume(self.diskSize, self.tag)

    def tearDown(self):
        stratusDeleteVolume(self.uuid)

    def test_usecase(self):
        stratusDescribeVolumes(self.uuid)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicPersistentDiskLifecycle)
