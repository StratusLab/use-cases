
import unittest
import time

from stratuslab_usecases.cli.TestUtils import sshConnectionOrTimeout, ssh

import BasicVmLifecycleTestBase


class testPersistentDiskRetainsData(BasicVmLifecycleTestBase.BasicVMsDiskTestBase):
    vmNum = 2
    vmName = 'ubuntu'
    timeout = 15*60

    def test_usecase(self):
        for i in xrange(self.vmNum):
            sshConnectionOrTimeout(self.ip_addresses[i][0], timeout=4*60)
            # Ensure kernel module is available for dynamic disk attachment
            ssh(ip=self.ip_addresses[i][0], cmd='modprobe acpiphp')

        # Attach disk to first machine.
        retval = self.driver.attach_volume(self.nodes[0], self.volume)
        self.assertTrue(retval, 'Failed to attach volume %s to node %s' %
                        (self.volume, self.nodes[0]))
        print 'attach:', self.volume

        # Format disk and add data file.
        ssh(ip=self.ip_addresses[0][0], cmd='mkfs.ext3 /dev/vda')
        ssh(ip=self.ip_addresses[0][0], cmd='mkdir -p /mnt/pdisk')
        ssh(ip=self.ip_addresses[0][0], cmd='mount -t ext3 /dev/vda /mnt/pdisk')
        ssh(ip=self.ip_addresses[0][0], cmd='touch /mnt/pdisk/data_file')
        ssh(ip=self.ip_addresses[0][0], cmd='umount /mnt/pdisk')

        # Detach disk from machine.
        retval = self.driver.detach_volume(self.volume)
        self.assertTrue(retval, '%s: Failed to detach volume' % self.volume)
        print 'detach:', self.volume
        time.sleep(5)

        # Attach disk to second machine and ensure data file exists.
        retval = self.driver.attach_volume(self.nodes[1], self.volume)
        self.assertTrue(retval, 'Failed to attach volume %s to node %s' %
                        (self.volume, self.nodes[1]))
        print 'attach:', self.volume
        time.sleep(5)
        ssh(ip=self.ip_addresses[1][0], cmd='mkdir -p /mnt/pdisk')
        ssh(ip=self.ip_addresses[1][0], cmd='mount -t ext3 /dev/vda /mnt/pdisk')
        ssh(ip=self.ip_addresses[1][0], cmd='ls -l /mnt/pdisk/data_file')

        # Detach disk from machine.
        retval = self.driver.detach_volume(self.volume)
        self.assertTrue(retval, '%s: Failed to detach volume' % self.volume)
        print 'detach:', self.volume
        time.sleep(5)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testPersistentDiskRetainsData)
