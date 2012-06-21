import time
import unittest
import os, os.path

from usecases.TestUtils import *

class testPersistentDiskRetainsData(unittest.TestCase):

    # minimal ubuntu image
    marketplaceId = 'HZTKYZgX7XzSokCHMB60lS0wsiv'

    diskSize = 1

    def setUp(self):
        self.uuid = stratusCreateVolume(self.diskSize)
        self.vm_id_1, self.vm_ip_1 = stratusRunInstance(self.marketplaceId)
        self.vm_id_2, self.vm_ip_2 = stratusRunInstance(self.marketplaceId)

    def tearDown(self):
        stratusKillInstance(self.vm_id_1)
        stratusKillInstance(self.vm_id_2)
        time.sleep(5)
        stratusDeleteVolume(self.uuid)

    def test_usecase(self):
        waitVmRunningOrTimeout(self.vm_id_1, timeout=(10*60))
        waitVmRunningOrTimeout(self.vm_id_2, timeout=(10*60))
        sshConnectionOrTimeout(self.vm_ip_1)
        sshConnectionOrTimeout(self.vm_ip_2)

        # Ensure kernel module is available for dynamic disk attachment
        ssh(ip=self.vm_ip_1, cmd='modprobe acpiphp')
        ssh(ip=self.vm_ip_2, cmd='modprobe acpiphp')

        # Attach disk to first machine.
        stratusAttachVolume(self.vm_id_1, self.uuid)

        # Format disk and add data file.
        ssh(ip=self.vm_ip_1, cmd='mkfs.ext3 /dev/vda')
        ssh(ip=self.vm_ip_1, cmd='mkdir -p /mnt/pdisk')
        ssh(ip=self.vm_ip_1, cmd='mount -t ext3 /dev/vda /mnt/pdisk')
        ssh(ip=self.vm_ip_1, cmd='touch /mnt/pdisk/data_file')
        ssh(ip=self.vm_ip_1, cmd='umount /mnt/pdisk')

        # Detach disk from machine.
        stratusDetachVolume(self.vm_id_1, self.uuid)
        time.sleep(5)

        # Attach disk to second machine and ensure data file exists.
        stratusAttachVolume(self.vm_id_2, self.uuid)        
        time.sleep(5)
        ssh(ip=self.vm_ip_2, cmd='mkdir -p /mnt/pdisk')
        ssh(ip=self.vm_ip_2, cmd='mount -t ext3 /dev/vda /mnt/pdisk')
        ssh(ip=self.vm_ip_2, cmd='ls -l /mnt/pdisk/data_file')

        # Detach disk from machine.
        stratusDetachVolume(self.vm_id_2, self.uuid)
        time.sleep(5)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testPersistentDiskRetainsData)
