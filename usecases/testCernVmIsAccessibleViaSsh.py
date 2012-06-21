import unittest
import os, os.path

from usecases.TestUtils import *

class testVmIsAccessibleViaSsh(unittest.TestCase):

    # unmodified CernVM batch mode
    marketplaceId = 'HNfftwl2c-DkCVJW8eLUXETtarB'

    def setUp(self):
        self.vm_id, self.vm_ip = stratusRunInstance(self.marketplaceId)

    def tearDown(self):
        stratusKillInstance(self.vm_id)

    def test_usecase(self):
        waitVmRunningOrTimeout(self.vm_id, timeout=(10*60))
        sshConnectionOrTimeout(self.vm_ip)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testVmIsAccessibleViaSsh)
