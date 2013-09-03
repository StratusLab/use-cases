import os, os.path
import unittest

from stratuslab_usecases.cli.TestUtils import *

class testDownloadImageFromMarketplace(unittest.TestCase):

    def setUp(self):
        self.file_descriptor, self.filename = tempfile.mkstemp()
        print "File info: %d, %s" % (self.file_descriptor, self.filename)

    def tearDown(self):
        closeFileDescriptorReliably(self.file_descriptor)
        removeFile(self.filename)

    def test_usecase(self):
        mkplace_uri = vm_image_info['ttylinux']['mkplace-uri']
        print 'Image URL: %s' % mkplace_uri
        stratusDownloadImage(mkplace_uri, self.filename)
        bytes = os.path.getsize(self.filename)
        print 'Image size: %d' % bytes
        self.assertTrue(bytes > 0)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testDownloadImageFromMarketplace)
