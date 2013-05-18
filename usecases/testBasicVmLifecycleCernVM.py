import unittest
import os, os.path

from usecases.TestUtils import *

class testBasicVmLifecycle(unittest.TestCase):

    vm_image_info = getVmImageInfo()
    marketplaceId = vm_image_info['cernvm']['id']

    def setUp(self):
        self.vm_id, self.vm_ip = stratusRunInstance(self.marketplaceId)

    def tearDown(self):
        stratusKillInstance(self.vm_id)

    def test_usecase(self):
        # Use an excessively long timeout because the download from
        # CERN can be incredibly slow. 
        waitVmRunningOrTimeout(self.vm_id, timeout=(20*60))

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicVmLifecycle)
