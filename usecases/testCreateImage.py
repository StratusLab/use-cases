import random
import time
import unittest
import os, os.path

from usecases.TestUtils import *

class testCreateImage(unittest.TestCase):

    vm_image_info = getVmImageInfo()
    ubuntu_id = vm_image_info['ubuntu']['id']

    vm_id = None
    vm_id_webserver = None
    vm_ip_webserver = None
    tag = 'test-' + str(random.uniform(1000,9999))

    image_uuid = None

    diskSize = 1

    def setUp(self):
        pass

    def tearDown(self):
        stratusKillInstance(self.vm_id)
        stratusKillInstance(self.vm_id_webserver)
        time.sleep(5)
        stratusDeleteVolume(self.image_uuid)

    def test_usecase(self):

        self.vm_id, self.vm_ip = stratusRunInstance(self.ubuntu_id, 
                                                    options=["--save",
                                                             "--title=%s" % self.tag,
                                                             "--comment=none",
                                                             "--author=joe.builder",
                                                             "--author-email=noreply@example.org",
                                                             "--image-version=0.1"])

        waitVmRunningOrTimeout(self.vm_id)
        sshConnectionOrTimeout(self.vm_ip, timeout=(10*60))

        # Do machine configuration.
        ssh(ip=self.vm_ip, cmd='rm -f /lib/udev/rules.d/*net-gen*')
        ssh(ip=self.vm_ip, cmd='rm -f /etc/udev/rules.d/*net.rules')
        ssh(ip=self.vm_ip, cmd='apt-get update')
        ssh(ip=self.vm_ip, cmd='apt-get install -y apache2 chkconfig')
        ssh(ip=self.vm_ip, cmd='echo cloudy_weather_expected > /var/www/cloud.txt')

        # Shutdown the machine and start the image copy.
        stratusShutdownInstance(self.vm_id)

        # Ensure that the disk shows up in the storage service.
        self.image_uuid, self.webserver_id = findImageDiskOrTimeout(tag=self.tag)

        # Mark this as a live machine image.
        stratusUpdateVolume(self.image_uuid, ['--machine-image-live'])

        # Run the web server (from the persistent disk)
        self.vm_id_webserver, self.vm_ip_webserver = stratusRunInstance(self.image_uuid)
        waitVmRunningOrTimeout(self.vm_id_webserver)
        sshConnectionOrTimeout(self.vm_ip_webserver)

        # Get file from the web server.
        resp, content = getUrlOrTimeout("http://%s/cloud.txt" % self.vm_ip_webserver)

        # Kill the instance; sleep to be sure the clean up is done.
        stratusKillInstance(self.vm_id_webserver)
        time.sleep(5)

        if (not re.match(".*cloudy_weather_expected.*", content)):
            raise Exception("invalid content: %s" % content)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testCreateImage)
