
import unittest
import time

from stratuslab_usecases.cli.TestUtils import sshConnectionOrTimeout, ssh

import BasicVmLifecycleTestBase


class testAttachAndDetachDisk(BasicVmLifecycleTestBase.BasicVmTestBase):
    vmName = 'ubuntu'
    timeout = 15*60

    diskSize = 1  # in gigabytes

    def setUp(self):
        self.storageVolume = self.driver.create_volume(self.diskSize, self.name())
        try:
            super(testAttachAndDetachDisk, self).setUp()
        except KeyboardInterrupt:
            raise
        except:
            self.driver.destroy_volume(self.storageVolume)
            raise
        
    def tearDown(self):
        try:
            super(testAttachAndDetachDisk, self).tearDown()
            time.sleep(5)
        finally:
            self.driver.destroy_volume(self.storageVolume)

    def test_usecase(self):
        sshConnectionOrTimeout(self.ip_addresses[0], timeout=4*60)

        # Ensure kernel module is available for dynamic disk attachment
        ssh(ip=self.ip_addresses[0], cmd='modprobe acpiphp')

        # Attach and detach disk from machine.
        retval = self.driver.attach_volume(self.node, self.storageVolume)
        self.assertTrue(retval, 'Failed to attach volume %s to node %s' %
                        (self.storageVolume, self.node))
        print 'attach:', self.storageVolume
        time.sleep(5)
        retval = self.driver.detach_volume(self.storageVolume)
        self.assertTrue(retval, '%s: Failed to detach volume' % self.storageVolume)
        print 'detach:', self.storageVolume
        time.sleep(5)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testAttachAndDetachDisk)
