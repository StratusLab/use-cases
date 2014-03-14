
import unittest
import time

from stratuslab_usecases.cli.TestUtils import sshConnectionOrTimeout, ssh

import BasicVmLifecycleTestBase


class testKillReleasesAttachedDisk(BasicVmLifecycleTestBase.BasicVmTestBase):
    vmName = 'ubuntu'
    timeout = 15*60

    diskSize = 1  # in gigabytes

    def setUp(self):
        self.storageVolume = self.driver.create_volume(self.diskSize, self.name())
        try:
            super(self.__class__, self).setUp()
        except KeyboardInterrupt:
            raise
        except:
            self.driver.destroy_volume(self.storageVolume)
            raise
        
    def tearDown(self):
        try:
            super(self.__class__, self).tearDown()
            time.sleep(5)
        except:
            pass
        if hasattr(self, 'storageVolume'):
            try:
                self.driver.detach_volume(self.storageVolume)
                time.sleep(5)
            except:
                pass
            self.driver.destroy_volume(self.storageVolume)

    def test_usecase(self):
        sshConnectionOrTimeout(self.ip_addresses[0], timeout=4*60)

        # Ensure kernel module is available for dynamic disk attachment
        ssh(ip=self.ip_addresses[0], cmd='modprobe acpiphp')

        # Attach disk to machine.
        retval = self.driver.attach_volume(self.node, self.storageVolume)
        self.assertTrue(retval, 'Failed to attach volume %s to node %s' %
                        (self.storageVolume, self.node))
        print 'attach:', self.storageVolume
        time.sleep(5)

        # Ensure that disk is visible in the machine.
        ssh(ip=self.ip_addresses[0], cmd='cat /proc/partitions')
        ssh(ip=self.ip_addresses[0], cmd='grep vda /proc/partitions')

        # Kill the machine.
        super(self.__class__, self).tearDown()
        time.sleep(15)

        # Now delete the volume. This is possible only if all of the mounts are removed.
        self.driver.destroy_volume(self.storageVolume)

        # If the delete worked, then del storageVolume attribute so the tear down doesn't fail.
        del self.storageVolume


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testKillReleasesAttachedDisk)
