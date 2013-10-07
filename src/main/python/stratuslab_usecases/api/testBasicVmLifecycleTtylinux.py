import unittest

import BasicVmLifecycleTestBase

class testBasicVmLifecycle(BasicVmLifecycleTestBase.BasicVmLifecycleTestBase):

    vmName = 'ttylinux'

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicVmLifecycle)
