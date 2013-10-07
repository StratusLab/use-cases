import unittest

from stratuslab_usecases.api import TestUtils

class BasicVmLifecycleTestBase(TestUtils.TestBase):

    @classmethod
    def name(cls):
        return cls.vmName

    size = None
    for s in TestUtils.TestBase.driver.list_sizes():
        if s.id == 'm1.medium': size = s; break
    location = None
    for l in TestUtils.TestBase.driver.list_locations():
        if l.id == 'default': location = l; break

    def setUp(self):
        images = [i for i in self.driver.list_images() if i.name.find(self.name()) != -1]
        self.image = images[-1]
        self.node = self.driver.create_node(name = self.name() + '-libcloud-node',
                                            size = self.size,
                                            location = self.location,
                                            image = self.image)

    def tearDown(self):
        self.driver.destroy_node(self.node)

    def test_usecase(self):
        self.driver.wait_until_running([self.node])
        print 'running:', self.node
