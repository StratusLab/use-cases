import os, os.path
import re
import unittest
import gzip

from usecases.TestUtils import *

class testUploadDisk(unittest.TestCase):

    def setUp(self):
        self.file_descriptor, self.filename = createDummyImage()

        print "File info: %d, %s" % (self.file_descriptor, self.filename)

    def tearDown(self):
        closeFileDescriptorReliably(self.file_descriptor)
        removeFile(self.filename)

    def test_usecase(self):

        url = stratusUploadImage(self.filename)
        print 'Uploaded disk URL: %s' % url

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testUploadDisk)
