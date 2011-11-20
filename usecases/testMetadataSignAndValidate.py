import unittest
import os, os.path

from usecases.TestUtils import *

class testMetadataSignAndValidate(unittest.TestCase):

    def setUp(self):
        self.file_descriptor, self.filename = createDummyImage()
        print "File info: %d, %s" % (self.file_descriptor, self.filename)

    def tearDown(self):
        closeFileDescriptorReliably(self.file_descriptor)
        removeFile(self.filename)
        removeFile(self.metadata)
        removeFile(self.metadata + ".orig")

    def test_sign_and_validate(self):
        stratusBuildMetadata(self.filename)
        self.metadata = expectedMetadataFilename()
        if (not os.path.exists(self.metadata)):
            raise Exception("expected metadata file %s does not exist" % self.metadata)

        try:
            stratusValidateMetadata(self.metadata)
        except Exception as e:
            print 'Got expected exception.'

        stratusSignMetadata(self.metadata)
        stratusValidateMetadata(self.metadata)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(testMetadataSignAndValidate)
