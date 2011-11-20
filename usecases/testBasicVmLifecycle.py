import unittest
import os, os.path

from usecases.TestUtils import *

class testBasicVmLifecycle(unittest.TestCase):

    marketplaceId = 'LwcRbwCalYSysY1wftQdAj6Bwoi'

    def setUp(self):
        self.vm_id, self.vm_ip = stratusRunInstance(self.marketplaceId)

    def tearDown(self):
        stratusKillInstance(self.vm_id)

    def test_basic_vm_lifecycle(self):
        waitVmRunningOrTimeout(self.vm_id)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(testClientVersionOption)
