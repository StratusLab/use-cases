import unittest

from stratuslab_usecases.api import testBasicPersistentDiskLifecycle as withoutTag

class testBasicPersistentDiskLifecycle(withoutTag.testBasicPersistentDiskLifecycle):
    
    tag = '"tag\'with}very\\\\dangerous\\"characters\\"'

    @classmethod
    def name(cls):
        return cls.tag

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testBasicPersistentDiskLifecycle)
