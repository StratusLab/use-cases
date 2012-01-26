import unittest
import os, os.path

from usecases.TestUtils import *

class testVmIsAccessibleViaSsh(unittest.TestCase):

    # minimal ttylinux image
    marketplaceId = 'PvitUfM-uW2yWakWUNmd-TSPOiy'

    def setUp(self):
        self.vm_id, self.vm_ip = stratusRunInstance(self.marketplaceId)

    def tearDown(self):
        stratusKillInstance(self.vm_id)

    def test_usecase(self):
        waitVmRunningOrTimeout(self.vm_id)
        sshConnectionOrTimeout(self.vm_ip)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testVmIsAccessibleViaSsh)
