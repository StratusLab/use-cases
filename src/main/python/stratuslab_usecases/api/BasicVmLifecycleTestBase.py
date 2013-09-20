import unittest

from libcloud.compute.providers import set_driver
from libcloud.compute.providers import get_driver

class BasicVmLifecycleTestBase(unittest.TestCase):

    set_driver('stratuslab',
               'stratuslab.libcloud.compute_driver',
               'StratusLabNodeDriver')
    StratusLabDriver = get_driver('stratuslab')
    driver = StratusLabDriver('default')

    size = None
    for s in driver.list_sizes():
        if s.id == 'm1.medium': size = s; break
    location = None
    for l in driver.list_locations():
        if l.id == 'default': location = l; break

    def setUp(self):
        images = [i for i in self.driver.list_images() if i.name.find(self.name) != -1]
        self.image = images[-1]
        self.node = self.driver.create_node(name = self.name + '-libcloud-node',
                                            size = self.size,
                                            location = self.location,
                                            image = self.image)

    def tearDown(self):
        self.driver.destroy_node(self.node)

    def test_usecase(self):
        self.driver.wait_until_running([self.node])
        print self.node
