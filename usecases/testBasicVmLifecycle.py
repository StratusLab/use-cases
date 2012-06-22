import unittest
import os, os.path

from usecases.TestUtils import *

class testBasicVmLifecycle(unittest.TestCase):

    # minimal ttylinux image
    marketplaceId = 'BN1EEkPiBx87_uLj2-sdybSI-Xb'

    def setUp(self):
        self.vm_id, self.vm_ip = stratusRunInstance(self.marketplaceId)

    def tearDown(self):
        stratusKillInstance(self.vm_id)

    def test_usecase(self):
        waitVmRunningOrTimeout(self.vm_id)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicVmLifecycle)
