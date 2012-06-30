import time
import unittest
import os, os.path

from usecases.TestUtils import *

class testRunVmFromPersistentDisk(unittest.TestCase):

    vm_image_info = getVmImageInfo()
    ttylinux_url = vm_image_info['ttylinux']['url']
    marketplaceId = vm_image_info['ubuntu']['id']

    vm_id = None
    vm_id_ttylinux = None

    diskSize = 1

    def setUp(self):
        self.uuid = stratusCreateVolume(self.diskSize)
        self.vm_id, self.vm_ip = stratusRunInstance(self.marketplaceId)

    def tearDown(self):
        stratusKillInstance(self.vm_id)
        stratusKillInstance(self.vm_id_ttylinux)
        time.sleep(5)
        stratusDeleteVolume(self.uuid)

    def test_usecase(self):
        waitVmRunningOrTimeout(self.vm_id)
        sshConnectionOrTimeout(self.vm_ip, timeout=(4*60))

        # Ensure kernel module is available for dynamic disk attachment
        ssh(ip=self.vm_ip, cmd='modprobe acpiphp')

        # Attach disk to machine.
        stratusAttachVolume(self.vm_id, self.uuid)

        # Copy ttylinux image onto persistent disk
        ssh(ip=self.vm_ip, cmd='apt-get install -y curl')
        ssh(ip=self.vm_ip, cmd='fdisk -l')
        ssh(ip=self.vm_ip, cmd='curl -o /tmp/ttylinux.img.gz %s' % self.ttylinux_url)
        ssh(ip=self.vm_ip, cmd='gunzip /tmp/ttylinux.img.gz')
        ssh(ip=self.vm_ip, cmd='dd if=/tmp/ttylinux.img of=/dev/vda')

        # Detach disk from machine.
        stratusDetachVolume(self.vm_id, self.uuid)
        time.sleep(5)

        # Mark this as a live machine image.
        stratusUpdateVolume(self.uuid, ['--machine-image-live'])

        # Run ttylinux from persistent disk
        self.vm_id_ttylinux, self.vm_ip_ttylinux = stratusRunInstance(self.uuid)
        waitVmRunningOrTimeout(self.vm_id_ttylinux)
        sshConnectionOrTimeout(self.vm_ip_ttylinux)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testRunVmFromPersistentDisk)
