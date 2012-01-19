import os
import unittest2 as unittest
from plone.app.testing import TEST_USER_ID
from base import INTEGRATION_TESTING

class TestNextPrevious(unittest.TestCase):
    """ Test the nextprevious adapter """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_creditload(self):
        # Assert that our user has no credit
        member = self.portal.restrictedTraverse(
            '@@plone_portal_state').member()
        self.assertEqual(member.getProperty('credits'), 0)

        # Test that we have a browser view for adding credits
        view = self.portal.restrictedTraverse('@@emas-credits')

        # Buy some credits
        # XXX This test will need TLC when the payment gateway is implemented
        # another reason to make it pluggable, so you can plug in a
        # null implementation for testing.
        request = self.layer['request']
        request["buy"] = "31415"
        view()

        # Assert that this worked
        member = self.portal.restrictedTraverse(
            '@@plone_portal_state').member()
        self.assertEqual(member.getProperty('credits'), 31415)
