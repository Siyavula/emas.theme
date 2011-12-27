import os
import unittest2 as unittest

from zope.component import createObject
from zope.filerepresentation.interfaces import IRawWriteFile

from Products.CMFCore.utils import getToolByName

from emas.theme.marshal import CNXMLWriteFile

from base import PROJECTNAME
from base import INTEGRATION_TESTING

dirname = os.path.dirname(__file__)

class TestMarshal(unittest.TestCase):
    """ Test marshal module """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_cnxmlwritefile(self):
        cnxml = open(os.path.join(dirname, 'test.cnxml')).read()

        xmlfile = createObject('rhaptos.xmlfile.xmlfile', id='test.cnxml')
        writer = IRawWriteFile(xmlfile, None)
        writer.write(cnxml)
        self.assertTrue(isinstance(writer, CNXMLWriteFile))
        writer.close()
        self.assertEquals(xmlfile.title, u'Calculating Descriptive Statistics')
        self.assertEquals(xmlfile.body.raw, cnxml)

