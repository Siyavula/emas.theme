import lxml
import transaction
from datetime import datetime, date, timedelta
import unittest2 as unittest
from DateTime import DateTime
from emas.theme.tests.base import BaseFunctionalTestCase

from zExceptions import Unauthorized
from zope.component import queryUtility
from zope.publisher.browser import TestRequest
from z3c.relationfield.relation import create_relation

from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from plone.dexterity.utils import createContentInContainer

from emas.theme.interfaces import IEmasSettings
from emas.app.member_service import IMemberService
from emas.app.service import IService
from emas.theme.browser.practice import IPractice, Practice


class TestMxitPaymentRequest(BaseFunctionalTestCase):
    
    def setUp(self):
        super(TestMxitPaymentRequest, self).setUp()
        settings = queryUtility(IRegistry).forInterface(IEmasSettings)

    def test_logged_in(self):
        self.fail()
        
    def test_not_logged_in(self):
        self.logout()
        self.fail()


class TestMxitPaymentResponse(BaseFunctionalTestCase):
    
    def setUp(self):
        super(TestMxitPaymentResponse, self).setUp()
        settings = queryUtility(IRegistry).forInterface(IEmasSettings)
        
    def test_logged_in(self):
        self.fail()
        
    def test_not_logged_in(self):
        self.logout()
        self.fail()


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMxitPaymentRequest))
    suite.addTest(unittest.makeSuite(TestMxitPaymentResponse))
    return suite
