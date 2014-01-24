
import unittest

import BasicVmLifecycleTestBase


class testBasicVmLifecycle(BasicVmLifecycleTestBase.BasicVmLifecycleTestBase):
    vmName = 'cernvm'
    timeout = 20*60


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicVmLifecycle)
