import os
import unittest2 as unittest

from base import INTEGRATION_TESTING
from Products.PortalTransforms.data import datastream

from emas.theme.transforms.cnxmlplus2cnxml import cnxmlplus_to_cnxml
from rhaptos.cnxmltransforms.cnxml2html import cnxml_to_html

dirname = os.path.dirname(__file__)

class TestTransforms(unittest.TestCase):
    """ Test transforms """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_cnxmlplus2cnxml(self):
        cnxmlplus = open(os.path.join(dirname, 'test.cnxmlplus')).read()
        transform = cnxmlplus_to_cnxml()
        data = datastream('cnxml')
        data = transform.convert(cnxmlplus, data) 

    def test_cnxml2shortcodehtml(self):
        cnxml = open(os.path.join(dirname, 'test.cnxml')).read()
        transform = cnxml_to_html()
        data = datastream('cnxml')
        data = transform.convert(cnxml, data) 
