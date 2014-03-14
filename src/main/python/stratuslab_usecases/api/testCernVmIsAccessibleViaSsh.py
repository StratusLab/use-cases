
import unittest

import BasicVmLifecycleTestBase


class testVmIsAccessibleViaSsh(BasicVmLifecycleTestBase.VmIsAccessibleViaSshTestBase):
    vmName = 'cernvm'
    timeout = 20*60
    sshTimeout = 5*60


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testVmIsAccessibleViaSsh)
