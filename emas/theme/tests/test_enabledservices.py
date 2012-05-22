from datetime import datetime, timedelta
import os
import unittest2 as unittest
from base import INTEGRATION_TESTING

from zope.event import notify

from AccessControl import getSecurityManager
from Products.PluggableAuthService.events import PrincipalCreated

dirname = os.path.dirname(__file__)


class TestEnabledServices(unittest.TestCase):
    """ Test the pay service views  """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.context = self.portal
        self.request = self.portal.REQUEST
        user = getSecurityManager().getUser()
        # create transactions folder for test user
        notify(PrincipalCreated(user))
    
    def updateProperty(self, prop, value):
        member = self.context.restrictedTraverse(
            '@@plone_portal_state').member()
        member.setMemberProperties({prop: value})
    
    def test_is_enabled(self):
        pass

    def test_ask_expert_enabled(self):
        view = self.context.restrictedTraverse('@@enabled-services')
        self.assertTrue(
            view.ask_expert_enabled == True,
            'The "ask expert" service should be enabled.')
        
        self.updateProperty('askanexpert_registrationdate',
            datetime.date(datetime.now()))
        self.updateProperty('askanexpert_expirydate',
            datetime.date(datetime.now() + timedelta(days=30)))
        # buy some credits
        credits_view = self.portal.restrictedTraverse('@@emas-credits')
        request = self.layer['request']
        request["buy"] = "10"
        credits_view()
        self.assertTrue(
            view.ask_expert_enabled == True,
            'The "ask expert" service should now be enabled.')

    def test_answer_database_enabled(self):
        view = self.context.restrictedTraverse('@@enabled-services')
        self.assertTrue(
            view.answer_database_enabled == True,
            'The "answer database" service should be enabled.')
        
        self.updateProperty('answerdatabase_registrationdate',
            datetime.date(datetime.now()))
        self.updateProperty('answerdatabase_expirydate',
            datetime.date(datetime.now() + timedelta(days=30)))
        self.assertTrue(
            view.answer_database_enabled == True,
            'The "answer database" service should now be enabled.')

    def test_more_exercise_enabled(self):
        view = self.context.restrictedTraverse('@@enabled-services')
        self.assertTrue(
            view.more_exercise_enabled == True,
            'The "more exercise" service should be enabled.')
        
        self.updateProperty('moreexercise_registrationdate',
            datetime.date(datetime.now()))
        self.updateProperty('moreexcercise_expirydate',
            datetime.date(datetime.now() + timedelta(days=30)))
        self.assertTrue(
            view.more_exercise_enabled == True,
            'The "more exercise" service should now be enabled.')
