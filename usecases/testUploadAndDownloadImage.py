import os, os.path
import re
import unittest
import gzip

from usecases.TestUtils import *

class testUploadAndDownloadImage(unittest.TestCase):

    def setUp(self):
        self.file_descriptor, self.filename = createDummyImage()

        print "File info: %d, %s" % (self.file_descriptor, self.filename)

    def tearDown(self):
        closeFileDescriptorReliably(self.file_descriptor)
        removeFile(self.filename)

    def test_usecase(self):

        url = stratusUploadImage(self.filename)
        print 'Uploaded disk URL: %s' % url

        # Download the image to make sure it is accessible.
        # Eventually this should check that the downloaded file
        # is identical to the uploaded one, but this requires
        # that the server perserve the exact file size. 
        download_url = "%s?media=gzip" % url
        try:
            fd = wget(download_url)
            fd.read(100)
        finally:
            fd.close()

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testUploadAndDownloadImage)
