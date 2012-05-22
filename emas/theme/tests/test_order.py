import os
import unittest2 as unittest
from plone.app.testing import TEST_USER_ID
from base import INTEGRATION_TESTING

from zope.component import getSiteManager
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from AccessControl import getSecurityManager


class TestOrderForm(unittest.TestCase):
    """ Test the nextprevious adapter """
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
        self.assertEqual(orderform.totalcost, 150)
        self.assertEqual(orderform.packages,
            [u'1 year subscription to Intelligent Practice for Maths Grade 10'])

        # place an order for maths and textbook
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Maths"
        request["practice_grade"] = "Grade 10"
        request["include_textbook"] = "yes"
        request["include_expert_answers"] = "no"

        orderform()
        self.assertEqual(orderform.totalcost, 200)
        self.assertEqual(orderform.packages,
            [u'1 year subscription to Intelligent Practice for Maths Grade 10',
             u'Printed textbook for Maths Grade 10'])

        # place an order for science and expert answers
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Science"
        request["practice_grade"] = "Grade 10"
        request["include_textbook"] = "no"
        request["include_expert_answers"] = "yes"

        orderform()
        self.assertEqual(orderform.totalcost, 175)
        self.assertEqual(orderform.packages,
            [u'1 year subscription to Intelligent Practice for Science Grade 10',
             u'Expert answers to 10 of your questions'])


        # place an order for maths and science only
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Maths,Science"
        request["practice_grade"] = "Grade 10"
        request["include_textbook"] = "no"
        request["include_expert_answers"] = "no"

        orderform()
        self.assertEqual(orderform.totalcost, 250)
        self.assertEqual(orderform.packages,
            [(u'1 year subscription to Intelligent Practice for '
                'Maths and Science Grade 10')])

        # place an order for everything
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Maths,Science"
        request["practice_grade"] = "Grade 10"
        request["include_textbook"] = "yes"
        request["include_expert_answers"] = "yes"

        orderform()
        self.assertEqual(orderform.totalcost, 375)
        self.assertEqual(orderform.packages,
            [(u'1 year subscription to Intelligent Practice for '
                'Maths and Science Grade 10'),
             u'Printed textbook for Maths and Science Grade 10',
             u'Expert answers to 10 of your questions',
            ])

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

