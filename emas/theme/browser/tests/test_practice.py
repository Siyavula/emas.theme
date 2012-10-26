import unittest
import unittest2 as unittest
from base import BaseFunctionalTestCase

from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from emas.theme.interfaces import IEmasSettings
from emas.theme.browser.practice import IPractice, Practice

class TestPractice(BaseFunctionalTestCase):
    
    def afterSetUp(self):
        settings = queryUtility(IRegistry).forInterface(IEmasSettings)
        settings.practiceurl = u'http://localhost:37183'
        
    def test_not_logged_in(self):
        self.logout()
        view = self.portal.restrictedTraverse('@@practice')
        result = view()

    def test_logged_in_and_expired(self):
        self.fail()

    def test_logged_in_not_expired(self):
        self.fail()
    
    def test_logged_in_grade10_maths(self):
        self.fail()

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPractice))
    return suite
