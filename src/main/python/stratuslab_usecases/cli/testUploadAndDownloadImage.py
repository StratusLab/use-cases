import os, os.path
import re
import unittest
import gzip

from stratuslab_usecases.cli.TestUtils import *

class testUploadAndDownloadImage(unittest.TestCase):

    def setUp(self):
        self.file_descriptor, self.filename = createDummyImage()

        print "File info: %d, %s" % (self.file_descriptor, self.filename)

    def tearDown(self):
        closeFileDescriptorReliably(self.file_descriptor)
        removeFile(self.filename)

    def test_usecase(self):

        response = stratusUploadImage(self.filename)
        p = re.compile(r".*Image uploaded:\s*([^\s]+)$", re.DOTALL)
        m = p.match(response)
        if m:
            url = m.group(1)

            print 'Uploaded disk URL: %s' % url

            # Download the image to make sure it is accessible.
            # Eventually this should check that the downloaded file
            # is identical to the uploaded one, but this requires
            # that the server perserve the exact file size. 
            download_url = "%s?media=gzip" % url
            with wget(download_url) as fd:
                fd.read(100)
        else:
            raise Exception('No URL in response: %s' % response)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testUploadAndDownloadImage)
