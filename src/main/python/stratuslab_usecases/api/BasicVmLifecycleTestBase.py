from stratuslab_usecases.api import TestUtils
from stratuslab_usecases.cli.TestUtils import getVmImageInfo


class BasicVmLifecycleTestBase(TestUtils.TestBase):
    @classmethod
    def name(cls):
        return cls.vmName

    size = None
    for s in TestUtils.TestBase.driver.list_sizes():
        if s.id == 'm1.medium':
            size = s
            break

    location = None
    for l in TestUtils.TestBase.driver.list_locations():
        if l.id == 'default':
            location = l
            break

    sleepInterval = wait_period = 5 # How many seconds to between retries
    timeout = 2*60 # How many seconds to wait before timing out

    def setUp(self):
        marketplaceId = getVmImageInfo()[self.name()]['id']
        for i in self.driver.list_images():
            if i.id == marketplaceId:
                image = i
                print 'image:', image
                break

        self.node = self.driver.create_node(name=self.name() + '-libcloud-node',
                                            size=self.size,
                                            image=image,
                                            location=self.location)

    def tearDown(self):
        retval = self.driver.destroy_node(self.node)
        self.assertTrue(retval, '%s: Failed to destroy node' % self.node)

    def test_usecase(self):
        node, _ = self.driver.wait_until_running([self.node],
                                                 wait_period=self.wait_period,
                                                 timeout=self.timeout)[0]
        self.assertEqual(node.uuid, self.node.uuid)
        self.assertEqual(node.image.id, self.node.image.id)
        print 'running:', self.node
