import time
import unittest
import os, os.path

from usecases.TestUtils import *

class testKillReleasesAttachedDisk(unittest.TestCase):

    # minimal ubuntu image
    marketplaceId = 'HZTKYZgX7XzSokCHMB60lS0wsiv'

    diskSize = 1

    def setUp(self):
        self.uuid = stratusCreateVolume(self.diskSize)
        self.vm_id_1, self.vm_ip_1 = stratusRunInstance(self.marketplaceId)

    def tearDown(self):
        stratusKillInstance(self.vm_id_1)
        time.sleep(5)
        stratusDetachVolume(self.vm_id_1, self.uuid)
        time.sleep(5)
        stratusDeleteVolume(self.uuid)

    def test_usecase(self):
        waitVmRunningOrTimeout(self.vm_id_1, timeout=(5*60))
        sshConnectionOrTimeout(self.vm_ip_1, timeout=(4*60))

        # Ensure kernel module is available for dynamic disk attachment
        ssh(ip=self.vm_ip_1, cmd='modprobe acpiphp')

        # Attach disk to machine.
        stratusAttachVolume(self.vm_id_1, self.uuid)
        time.sleep(5)

        # Ensure that disk is visible in the machine.
        ssh(ip=self.vm_ip_1, cmd='cat /proc/partitions')
        ssh(ip=self.vm_ip_1, cmd='grep vda /proc/partitions')

        # Kill the machine.
        stratusKillInstance(self.vm_id_1)
        time.sleep(5)

        # Now delete the volume.  This is possible only if all of the mounts are removed.
        stratusDeleteVolume(self.uuid)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testPersistentDiskRetainsData)
