import os, os.path
import unittest

from usecases.TestUtils import *

class testDownloadImage(unittest.TestCase):

    def setUp(self):
        self.file_descriptor, self.filename = tempfile.mkstemp()
        print "File info: %d, %s" % (self.file_descriptor, self.filename)

    def tearDown(self):
        closeFileDescriptorReliably(self.file_descriptor)
        removeFile(self.filename)

    def test_usecase(self):
        ttylinux_url = vm_image_info['ttylinux']['url']
        print 'Image URL: %s' % ttylinux_url
        stratusDownloadImage(ttylinux_url, self.filename)
        bytes = os.path.getsize(self.filename)
        print 'Image size: %d' % size
        self.assertTrue(bytes > 0)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testDownloadImage)