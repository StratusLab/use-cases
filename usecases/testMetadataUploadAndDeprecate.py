import os, os.path
import re
import unittest

from usecases.TestUtils import *

try:
    from lxml import etree
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree
                except ImportError:
                    raise Exception("Failed to import ElementTree from any known place")

class testMetadataUploadAndDeprecate(unittest.TestCase):

    def _getElement(self, tree, ns, name):
        xpath = ".//{%s}%s" % (ns, name)
        element = tree.find(xpath)
        if element is None:
            raise Exception("element (%s) was not found in metadata entry" % xpath)
        return element.text

    def setUp(self):
        self.file_descriptor, self.filename = createDummyImage()
        print "File info: %d, %s" % (self.file_descriptor, self.filename)

    def tearDown(self):
        closeFileDescriptorReliably(self.file_descriptor)
        removeFile(self.filename)
        removeFile(self.metadata)
        removeFile(self.metadata + ".orig")

    def test_usecase(self):

        stratusBuildMetadata(self.filename)
        self.metadata = expectedMetadataFilename()
        if (not os.path.exists(self.metadata)):
            raise Exception("expected metadata file %s does not exist" % self.metadata)

        stratusSignMetadata(self.metadata)
        stratusValidateMetadata(self.metadata)

        url = stratusUploadMetadata(self.metadata)
        print 'Original entry URL: %s' % url

        originalFile = open(self.metadata)
        originalXml = originalFile.read()
        originalFile.close()

        marketplaceXml = readRemoteXMLFile(url)

        # Strip leading and trailing whitespace.  They do not affect the
        # validity of the XML signature and these are often added/removed
        # in the various stages of processing.
        originalXml = originalXml.strip(originalXml)
        marketplaceXml = marketplaceXml.strip(marketplaceXml)

        self.assertEqual(originalXml, marketplaceXml, 
                         'original and Marketplace XML files are not identical')

        tree = etree.ElementTree()
        tree.parse(self.metadata)

        identifier = self._getElement(tree, 'http://purl.org/dc/terms/', 'identifier')
        print 'Marketplace Identifier: %s' % identifier

        parent = os.path.dirname(url)
        grandparent = os.path.dirname(parent)

        # Grandparent URL should provide a response. 
        _ = readRemoteXMLFile(grandparent)

        deprecatedUrl = stratusDeprecateMetadata(identifier, 'jane.tester@example.org')
        deprecatedEntry = readRemoteXMLFile(deprecatedUrl)
        deprecatedTree = etree.fromstring(deprecatedEntry)

        deprecatedReason = self._getElement(deprecatedTree, 
                                            'http://mp.stratuslab.eu/slterms#', 
                                            'deprecated')

        self.assertEqual("Just For Fun", deprecatedReason)

        # After deprecating the entry, the grandparent URL should return nothing (i.e. 404)
        try:
            readRemoteXMLFile(grandparent)
        except urllib2.HTTPError as e:
            self.assertEqual(404, e.code, '%s did not give 404 error but %d instead' % 
                             (grandparent, e.code))

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testMetadataUploadAndDeprecate)
