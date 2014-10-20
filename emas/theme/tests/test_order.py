import unittest2 as unittest
from plone.app.testing import TEST_USER_ID

from zope.component import getSiteManager
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from AccessControl import getSecurityManager

from emas.theme.tests.base import INTEGRATION_TESTING

class TestOrderForm(unittest.TestCase):
    """ Test the order process """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.setupMailHost()
        state = self.portal.restrictedTraverse('@@plone_portal_state')
        member = state.member()
        member.setProperties({'fullname': 'Tester One',
                              'email': 'testerone@example.com'})

    def beforeTearDown(self):
        self.restoreMailHost()

    def test_orderform(self):
        orderform = self.portal.restrictedTraverse('@@order') 
        
        # render the form
        result = orderform()

        # place an order for maths only
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Maths"
        request["practice_grade"] = "Grade 10"
        request["include_textbook"] = "no"
        request["include_expert_answers"] = "no"

        orderform()

        # place an order for maths and textbook
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Maths"
        request["practice_grade"] = "Grade 10"
        request["include_textbook"] = "yes"
        request["include_expert_answers"] = "no"

        orderform()

        # place an order for science and expert answers
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Science"
        request["practice_grade"] = "Grade 10"
        request["include_textbook"] = "no"
        request["include_expert_answers"] = "yes"

        orderform()

        # place an order for maths and science only
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Maths,Science"
        request["practice_grade"] = "Grade 10"
        request["include_textbook"] = "no"
        request["include_expert_answers"] = "no"

        orderform()

        # place an order for everything
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Maths,Science"
        request["practice_grade"] = "Grade 10"
        request["include_textbook"] = "yes"
        request["include_expert_answers"] = "yes"

        orderform()

    def setupMailHost(self):
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

    def restoreMailHost(self):
        self.portal.MailHost = self.portal._original_MailHost
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(self.portal._original_MailHost), provided=IMailHost)

