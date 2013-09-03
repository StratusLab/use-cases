import unittest
import os, os.path

from stratuslab_usecases.cli.TestUtils import *

class testBasicVmLifecycle(unittest.TestCase):

    vm_image_info = getVmImageInfo()
    marketplaceId = vm_image_info['ttylinux']['id']

    def setUp(self):
        self.vm_id, self.vm_ip = stratusRunInstance(self.marketplaceId)

    def tearDown(self):
        stratusKillInstance(self.vm_id)

    def test_usecase(self):
        waitVmRunningOrTimeout(self.vm_id)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicVmLifecycle)
