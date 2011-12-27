import os
import unittest2 as unittest

from base import INTEGRATION_TESTING
from Products.PortalTransforms.data import datastream

from emas.theme.transforms.cnxmlplus2cnxml import cnxmlplus_to_cnxml

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

