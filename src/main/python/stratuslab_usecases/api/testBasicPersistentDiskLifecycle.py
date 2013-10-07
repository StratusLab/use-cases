import unittest

from stratuslab_usecases.api import TestUtils

class testBasicPersistentDiskLifecycle(TestUtils.TestBase):

    diskSize = 1 # in gigabytes

    def setUp(self):
        self.storageVolume = self.driver.create_volume(self.diskSize, self.name())
        #return StorageVolume(vol_uuid, name, size, self, extra=extra)
        #from libcloud.compute.base import StorageVolume

        #self.uuid = stratusCreateVolume(self.diskSize)

    def tearDown(self):
        self.driver.destroy_volume(self.storageVolume)

        #stratusDeleteVolume(self.uuid)

    def test_usecase(self):
        """Check attributes of created and listed disks.
        """
        self.assertEqual(self.name(), self.storageVolume.name)
        self.assertAlmostEqual(self.diskSize, self.storageVolume.size)
        print 'create:', self.storageVolume
        
        for v in self.driver.list_volumes(self.storageVolume.extra['location']):
            if v.id == self.storageVolume.id:
               self.assertEqual(v.name, self.storageVolume.name)
               self.assertAlmostEqual(v.size, self.storageVolume.size)
               print 'list:', v
               return
        self.fail('id %s: No such storage volume' % self.storageVolume.id)

        #stratusDescribeVolumes(self.uuid)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicPersistentDiskLifecycle)
