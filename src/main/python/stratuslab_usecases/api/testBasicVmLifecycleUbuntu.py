
import unittest

import BasicVmLifecycleTestBase


class testBasicVmLifecycle(BasicVmLifecycleTestBase.BasicVmLifecycleTestBase):
    vmName = 'ubuntu'
    timeout = 15*60


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicVmLifecycle)
