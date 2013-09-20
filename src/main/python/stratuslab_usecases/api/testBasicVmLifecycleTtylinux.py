import unittest

import BasicVmLifecycleTestBase

class testBasicVmLifecycle(BasicVmLifecycleTestBase.BasicVmLifecycleTestBase):

    name = 'ttylinux'

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicVmLifecycle)
