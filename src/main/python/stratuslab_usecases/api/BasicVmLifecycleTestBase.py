import sys
import time

from libcloud.compute.ssh import SSHClient, ParamikoSSHClient

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

    sleepInterval = wait_period = 5 # How many seconds to wait between retries
    timeout = 2*60 # How many seconds to wait before timing out

    def setUp(self):
        marketplaceId = getVmImageInfo()[self.name()]['id']
        for i in self.driver.list_images():
            if i.id == marketplaceId:
                image = i
                print 'image:', image
                break
        self.assertTrue('image' in locals(), 'id: %s: Image not found' % marketplaceId)

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


class BasicVmTestBase(BasicVmLifecycleTestBase):
    def setUp(self):
        super(BasicVmTestBase, self).setUp()
        try:
            _, self.ip_addresses = self.driver.wait_until_running(
                [self.node],
                wait_period=self.wait_period,
                timeout=self.timeout)[0]
            print 'ip_addresses:', self.ip_addresses
        except KeyboardInterrupt:
            raise
        except:
            super(BasicVmTestBase, self).tearDown()
            raise

    def test_usecase(self):
        raise NotImplementedError('test_usecase not implemented for class %s' %
                                  self.__class__.__name__)


class VmIsAccessibleViaSshTestBase(BasicVmTestBase):
    sshTimeout = 2*60 # How many seconds to wait before giving up on SSH connection
    sshConnectTimeout = 5 # ConnectTimeout as in ssh_config(5)

    def setUp(self):
        if not issubclass(SSHClient, ParamikoSSHClient):
            raise RuntimeError('paramiko is not installed. You can install ' +
                               'it using pip: pip install paramiko')

        super(VmIsAccessibleViaSshTestBase, self).setUp()

    def test_usecase(self):
        client = SSHClient(hostname=self.ip_addresses[0],
                           timeout=self.sshConnectTimeout)
        self.driver._ssh_client_connect(ssh_client=client,
                                        wait_period=self.wait_period,
                                        timeout=self.sshTimeout)
        cmd = '/bin/true'
        stdout, stderr, status = client.run(cmd)
        client.close()
        self.assertEqual(status, 0)
        print 'execute:', cmd


class BasicVMsTestBase(TestUtils.TestBase):
    vmNum = 1
    
    @classmethod
    def name(cls):
        return cls.vmName

    vmSize = 'm1.medium'
    size = None
    for s in TestUtils.TestBase.driver.list_sizes():
        if s.id == vmSize:
            size = s
            break

    vmLocation = 'default'
    location = None
    for l in TestUtils.TestBase.driver.list_locations():
        if l.id == vmLocation:
            location = l
            break

    sleepInterval = wait_period = 5 # How many seconds to wait between retries
    timeout = 2*60 # How many seconds to wait before timing out

    def raiseErrs(self, errs=None):
        if errs is None and hasattr(self, 'errs'):
            errs = self.errs
        if errs:
            for i in xrange(len(errs) - 1):
                print >>sys.stderr, errs[i]
            raise errs[len(errs) - 1]

    def setUp(self):
        marketplaceId = getVmImageInfo()[self.name()]['id']
        for i in self.driver.list_images():
            if i.id == marketplaceId:
                image = i
                print 'image:', image
                break
        self.assertTrue('image' in locals(), 'id: %s: Image not found' % marketplaceId)

        self.nodes = list()
        self.ip_addresses = list()
        for i in xrange(self.vmNum):
            try:
                self.nodes.append(self.driver.create_node(
                    name=self.name() + '-libcloud-node',
                    size=self.size,
                    image=image,
                    location=self.location))
                print 'create:', self.nodes[i]
                self.ip_addresses.append(self.driver.wait_until_running(
                    [self.nodes[i]],
                    wait_period=self.wait_period,
                    timeout=self.timeout)[0][1])
                print 'ip_addresses:', self.ip_addresses[i]
            except KeyboardInterrupt:
                raise
            except:
                self.tearDown()
                raise

    def tearDown(self):
        if hasattr(self, 'nodes'):
            errs = []
            for n in self.nodes:
                try:
                    retval = self.driver.destroy_node(n)
                    self.assertTrue(retval, '%s: Failed to destroy node' % n)
                except KeyboardInterrupt:
                    raise
                except Exception, e:
                    errs.append(e)
            del self.nodes
            self.raiseErrs(errs)


class BasicDiskTestBase(TestUtils.TestBase):
    diskSize = 1  # in gigabytes

    def setUp(self):
        self.volume = self.driver.create_volume(self.diskSize, self.name())

    def tearDown(self):
        if hasattr(self, 'volume'):
            try:
                self.driver.destroy_volume(self.volume)
            finally:
                del self.volume


class BasicVMsDiskTestBase(BasicVMsTestBase, BasicDiskTestBase):
    def setUp(self):
        BasicDiskTestBase.setUp(self)
        try:
            BasicVMsTestBase.setUp(self)
        except KeyboardInterrupt:
            raise
        except:
            BasicDiskTestBase.tearDown(self)
            raise

    def tearDown(self):
        try:
            BasicVMsTestBase.tearDown(self)
            time.sleep(5)
        except KeyboardInterrupt:
            raise
        except:
            BasicDiskTestBase.tearDown(self)
            raise
        else:
            BasicDiskTestBase.tearDown(self)
