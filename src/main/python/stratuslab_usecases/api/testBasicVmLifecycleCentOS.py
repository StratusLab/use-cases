
import unittest

import BasicVmLifecycleTestBase


class testBasicVmLifecycle(BasicVmLifecycleTestBase.BasicVmLifecycleTestBase):
    vmName = 'centos'
    timeout = 10*60


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicVmLifecycle)
