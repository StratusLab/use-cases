from libcloud.compute.providers import set_driver
from libcloud.compute.providers import get_driver

import unittest

class StratusLabDriverHandle(object):

    set_driver('stratuslab',
               'stratuslab.libcloud.compute_driver',
               'StratusLabNodeDriver')
    StratusLabDriver = get_driver('stratuslab')
    driver = StratusLabDriver('default')

class TestBase(StratusLabDriverHandle, unittest.TestCase):

    @classmethod
    def name(cls):
        return cls.__name__
