
import unittest

import BasicVmLifecycleTestBase


class testVmIsAccessibleViaSsh(BasicVmLifecycleTestBase.VmIsAccessibleViaSshTestBase):
    vmName = 'centos'
    timeout = 10*60
    sshTimeout = 5*60


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testVmIsAccessibleViaSsh)
