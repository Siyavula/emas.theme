import os
import unittest2 as unittest
from plone.app.testing import TEST_USER_ID
from base import INTEGRATION_TESTING

from emas.theme.browser.practice import IPractice, Practice

class TestPractice(unittest.TestCase):
    """ Test the Practice browser view """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_call(self):
        request = self.layer['request']
        view = self.portal.restrictedTraverse('@@practice')
        self.assertTrue(IPractice.providedBy(view))
