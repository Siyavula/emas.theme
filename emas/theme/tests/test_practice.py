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

    def test_add_first_login_message_for_manager(self):
        self.fail()

    def test_add_first_login_message_for_member_no_services(self):
        self.fail()
        
    def test_add_first_login_message_for_member_with_services(self):
        self.fail()

    def test_services_active_for_manager(self):
        self.fail()

    def test_services_active_for_member_no_services(self):
        self.fail()

    def test_services_active_for_member_with_services(self):
        self.fail()

    def test_practice_service_messages_for_manager(self):
        self.fail()

    def test_practice_service_messages_for_member_all_services_expired(self):
        self.fail()

    def test_practice_service_messages_for_member_some_services_expired(self):
        self.fail()

    def test_format_date(self):
        self.fail()

    def test_format_date_this_year(self):
        self.fail()

    def test_format_date_next_year(self):
        self.fail()

    def test_number_of_days_until_expiry_in_past(self):
        self.fail()

    def test_number_of_days_until_expiry_in_1_day(self):
        self.fail()

    def test_number_of_days_until_expiry_in_2_day(self):
        self.fail()

    def test_number_of_days_until_expiry_next_year(self):
        self.fail()

    def test_expiring_services_none_expiring(self):
        self.fail()
    
    def test_expiring_services_serveral_expiring(self):
        self.fail()
    
    def test_active_services_none_active(self):
        self.fail()

    def test_active_services_several_active(self):
        self.fail()

    def test_is_expiring_expiring_yesterday(self):
        self.fail()

    def test_is_expiring_expiring_today(self):
        self.fail()

    def test_is_expiring_expiring_tomorrow(self):
        self.fail()

    def test_memberservice_expiry_threshold_trial_memberservices(self):
        self.fail()

    def test_memberservice_expiry_threshold_monthly_memberservices(self):
        self.fail()

    def test_memberservice_expiry_threshold_annual_memberservices(self):
        self.fail()

    def get_services_no_services(self):
        self.fail()

    def get_services(self):
        self.fail()

    def get_accessto(self):
        self.fail()

    def add_noaccess_message(self):
        self.fail()
