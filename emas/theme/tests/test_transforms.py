import os
import unittest2 as unittest

from base import INTEGRATION_TESTING
from Products.PortalTransforms.data import datastream
from Products.CMFCore.utils import getToolByName

from emas.theme.transforms.cnxmlplus2shortcodecnxml import cnxmlplus_to_shortcodecnxml
from emas.theme.transforms.shortcodehtml2html import shortcodehtml_to_html
from emas.theme.transforms.shortcodecnxml2shortcodehtml import \
    shortcodecnxml_to_shortcodehtml

dirname = os.path.dirname(__file__)

class TestTransforms(unittest.TestCase):
    """ Test transforms """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
    
    def test_cnxmlplus2shortcodecnxml_iotypes(self):
        transform = self.portal.portal_transforms['cnxmlplus_to_shortcodecnxml']
        self.assertEqual(
            transform.inputs[0], 'application/cnxmlplus+xml',
            'test_cnxmlplus2cnxml_iotypes: Input type wrong')
        self.assertEqual(
            transform.output, 'application/shortcodecnxml+xml',
            'test_cnxmlplus2cnxml_iotypes: Output type wrong')

    def test_cnxmlplus2cnxml(self):
        cnxmlplus = open(os.path.join(dirname, 'test.cnxmlplus')).read()
        transform = cnxmlplus_to_shortcodecnxml()
        data = datastream('cnxml')
        data = transform.convert(cnxmlplus, data) 

    def test_shortcodecnxml2shortcodehtml_iotypes(self):
        transform = self.portal.portal_transforms['shortcodecnxml_to_shortcodehtml']
        self.assertEqual(
            transform.inputs[0], 'application/shortcodecnxml+xml',
            'test_shortcodecnxml2shortcodehtml_iotypes: Input type wrong')
        self.assertEqual(
            transform.output, 'text/shortcodehtml',
            'test_cnxml2shortcodehtml_iotypes: Output type wrong')

    def test_shortcodecnxml2shortcodehtml(self):
        cnxml = open(os.path.join(dirname, 'test.cnxml')).read()
        transform = shortcodecnxml_to_shortcodehtml()
        data = datastream('cnxml')
        data = transform.convert(cnxml, data) 

    def test_shortcodehtml2html_iotypes(self):
        transform = self.portal.portal_transforms['shortcodehtml_to_html']
        self.assertEqual(
            transform.inputs[0], 'text/shortcodehtml',
            'test_shortcodehtml2html_iotypes: Input type wrong')
        self.assertEqual(
            transform.output, 'text/html',
            'test_shortcodehtml2html_iotypes: Output type wrong')

    def test_shortcodehtml2html(self):
        html = open(os.path.join(dirname, 'test.html')).read()
        transform = shortcodehtml_to_html()
        data = datastream(html)
        data = transform.convert(html, data) 

    def test_cnxmlplus2html_iotypes(self):
        transform = self.portal.portal_transforms['cnxmlplus_to_html_chain']
        self.assertEqual(
            transform.inputs[0], 'application/cnxmlplus+xml',
            'test_cnxmlplus2html_iotypes: Input type wrong')
        self.assertEqual(
            transform.output, 'text/html',
            'test_cnxmlplus2html_iotypes: Output type wrong')

    def _test_cnxmlplus2html_chain(self):
        """ This looks more like a functional than unittest since it exercises
            all the others too. Maybe we should move it.
        """
        cnxmlplus = open(os.path.join(dirname, 'test.cnxmlplus')).read()
        pt = getToolByName(self.portal, 'portal_transforms')
        transform = pt['cnxmlplus_to_html_chain']
        data = datastream(cnxmlplus)
        data = transform.convert(cnxmlplus, data) 
