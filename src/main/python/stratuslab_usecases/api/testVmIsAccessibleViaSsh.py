
import unittest

from stratuslab_usecases.cli.TestUtils import sshConnectionOrTimeout

import BasicVmLifecycleTestBase


class testVmIsAccessibleViaSsh(BasicVmLifecycleTestBase.BasicVmTestBase):
    vmName = 'ttylinux'

    def test_usecase(self):
        sshConnectionOrTimeout(self.ip_addresses[0])


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testVmIsAccessibleViaSsh)
