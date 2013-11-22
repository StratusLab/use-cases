import unittest

from stratuslab_usecases.api import TestUtils


class testBasicPersistentDiskLifecycle(TestUtils.TestBase):
    diskSize = 1  # in gigabytes

    def setUp(self):
        self.storageVolume = self.driver.create_volume(self.diskSize, self.name())

    def tearDown(self):
        self.driver.destroy_volume(self.storageVolume)

    def test_usecase(self):
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


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicPersistentDiskLifecycle)
