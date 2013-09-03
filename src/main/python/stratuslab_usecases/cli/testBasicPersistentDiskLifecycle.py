import unittest
import os, os.path

from stratuslab_usecases.cli.TestUtils import *

class testBasicPersistentDiskLifecycle(unittest.TestCase):

    diskSize = 1 # in gigabytes

    def setUp(self):
        self.uuid = stratusCreateVolume(self.diskSize)

    def tearDown(self):
        stratusDeleteVolume(self.uuid)

    def test_usecase(self):
        stratusDescribeVolumes(self.uuid)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicPersistentDiskLifecycle)
