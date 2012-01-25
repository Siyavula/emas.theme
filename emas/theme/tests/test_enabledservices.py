from DateTime import DateTime
import os
import unittest2 as unittest
from base import INTEGRATION_TESTING

dirname = os.path.dirname(__file__)


class TestEnabledServices(unittest.TestCase):
    """ Test the pay service views  """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.context = self.portal
        self.request = self.portal.REQUEST
    
    def updateProperty(self, prop, value):
        member = self.context.restrictedTraverse(
            '@@plone_portal_state').member()
        member.setMemberProperties({prop: value})
    
    def test_is_enabled(self):
        pass

    def test_ask_expert_enabled(self):
        view = self.context.restrictedTraverse('@@enabled-services')
        self.assertTrue(
            view.ask_expert_enabled == False,
            'The "ask expert" service should not be enabled yet.')
        
        self.updateProperty('askanexpert_registrationdate', DateTime())
        self.assertTrue(
            view.ask_expert_enabled == True,
            'The "ask expert" service should now be enabled.')

    def test_answer_database_enabled(self):
        view = self.context.restrictedTraverse('@@enabled-services')
        self.assertTrue(
            view.answer_database_enabled == False,
            'The "answer database" service should not be enabled yet.')
        
        self.updateProperty('answerdatabase_registrationdate', DateTime())
        self.assertTrue(
            view.answer_database_enabled == True,
            'The "answer database" service should now be enabled.')

    def test_more_exercise_enabled(self):
        view = self.context.restrictedTraverse('@@enabled-services')
        self.assertTrue(
            view.more_exercise_enabled == False,
            'The "more exercise" service should not be enabled yet.')
        
        self.updateProperty('moreexercise_registrationdate', DateTime())
        self.assertTrue(
            view.more_exercise_enabled == True,
            'The "more exercise" service should now be enabled.')
