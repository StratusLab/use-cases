
import unittest

from libcloud.compute.deployment import ScriptDeployment
from libcloud.compute.types import DeploymentError

from stratuslab_usecases.cli.TestUtils import getVmImageInfo

import testBasicVmLifecycleCentOS


class testBasicVmDeployment(testBasicVmLifecycleCentOS.testBasicVmLifecycle):

    def setUp(self):
        marketplaceId = getVmImageInfo()[self.name()]['id']
        for i in self.driver.list_images():
            if i.id == marketplaceId:
                image = i
                print 'image:', image
                break
        self.assertTrue('image' in locals(), 'id: %s: Image not found' % marketplaceId)
        self.image = image

    def tearDown(self):
        if hasattr(self,'node'):
            super(testBasicVmDeployment, self).tearDown()

    def test_usecase(self):
        script = ScriptDeployment('touch STRATUSLAB_DEPLOYMENT')
        try:
            self.node = self.driver.deploy_node(
                name=self.name() + '-libcloud-node',
                size=self.size,
                image=self.image,
                location=self.location,
                deploy=script,
                timeout=self.timeout)
        except DeploymentError, e:
            self.node = e.node
            raise

        self.assertEqual(self.image.id, self.node.image.id)
        print 'deploy:', self.node


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicVmDeployment)
