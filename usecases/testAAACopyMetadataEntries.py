import os, os.path
import unittest
import urllib2

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

class testAAACopyMetadataEntries(unittest.TestCase):

    primaryMarketplaceUrl = 'http://marketplace.stratuslab.eu/metadata/'

    def getEntriesToCopy(self):
        entriesToCopy = []
        for vm_name, info in getVmImageInfo().items():
            id = info['id']
            email = info['email']
            marketplace_id = "%s/%s" % (id, email)
            entriesToCopy.append(marketplace_id)
        return entriesToCopy

    def writeTempFile(self, contents):
        file_descriptor, filename = tempfile.mkstemp()

        file = None
        try:
            file = open(filename, 'w')
            file.write(contents)
        except Exception as e:
            print e
            raise e
        finally:
            closeFileReliably(file)

        closeFileDescriptorReliably(file_descriptor)

        return filename

    def test_usecase(self):

        for entry in self.getEntriesToCopy():

            # Contents are wrapped in a metadata root element. 
            # Be sure to remove this element during the processing.
            contents = readRemoteXMLFile("%s%s" % (self.primaryMarketplaceUrl, entry))

            tree = etree.fromstring(contents)

            rdf = tree.find('.//{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF')

            #endorsement = rdf.find('.//{http://mp.stratuslab.eu/slreq#}endorsement')
            #if not endorsement is None:
            #    endorsement.text = None
            #    endorsement.tail = None
            #    children = endorsement.findall('*')
            #    for child in children:
            #        endorsement.remove(child)

            #signatures = rdf.findall('{http://www.w3.org/2000/09/xmldsig#}Signature')
            #for signature in signatures:
            #    rdf.remove(signature)

            filename = self.writeTempFile(etree.tostring(rdf))

            print "FILENAME: " + filename

            stratusSignMetadata(filename)
            stratusValidateMetadata(filename)

            url = stratusUploadMetadata(filename)
            print 'Metadata entry URL: %s' % url

            os.remove(filename)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testAAACopyMetadataEntries)
