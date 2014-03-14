
import unittest

import BasicVmLifecycleTestBase


class testVmIsAccessibleViaSsh(BasicVmLifecycleTestBase.VmIsAccessibleViaSshTestBase):
    vmName = 'ubuntu'
    timeout = 15*60
    sshTimeout = 5*60


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testVmIsAccessibleViaSsh)
