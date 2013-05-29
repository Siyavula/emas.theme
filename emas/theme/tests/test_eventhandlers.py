import unittest2 as unittest
import lxml
from DateTime import DateTime

import zope.event
from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.events import PropertiesUpdated 

from emas.theme.tests.base import FUNCTIONAL_TESTING
from emas.theme.browser.tests.test_practice_service_messages_viewlet import \
    find_viewlet
from emas.theme.interfaces import IEmasThemeLayer
from emas.theme.eventhandlers import *


class TestEventhandlers(unittest.TestCase):
    """ Test the intelligent practice messages service viewlets  """

    layer = FUNCTIONAL_TESTING
    
    def setUp(self):
        super(TestEventhandlers, self).setUp()
        self.setRoles(['Reader',])
        self.context = self.portal.maths
        self.request = self.portal.REQUEST
        self.manager_name = 'plone.belowcontenttitle'
        self.themelayer = IEmasThemeLayer
        self.viewlet_name = 'emas.practice_service_messages'

    def test_first_login_message(self):
        portal_state = self.portal.restrictedTraverse('@@plone_portal_state')
        member = portal_state.member()
        self.setRoles('Owner')
        default = DateTime('2000/01/01')
        member.setProperties(login_time=default,
                             last_login_time=default)

        # The call to loginUser is the one that fires the required event.
        # The testcase's login method simly creates a new security manager, it
        # does not lead to the IUserLoggedInEvent. 
        pmt = getToolByName(self.portal, 'portal_membership')
        pmt.loginUser(self.portal.REQUEST)

        viewlet = find_viewlet(self.context,
                               self.request,
                               self.manager_name,
                               self.viewlet_name,
                               self.themelayer)

        result = viewlet.render()
        doc = lxml.html.fromstring(result)
        elements = doc.xpath('//a[contains(.,"@@practice")]')
        self.assertEqual(len(elements), 0,
                         'No link to @@practice found.')
    
    def test_onMemberPropsUpdates_subscribe(self):
        portal_state = self.portal.restrictedTraverse('@@plone_portal_state')
        member = portal_state.member()
        member.setProperties(subscribe_to_newsletter=True)
        event = PropertiesUpdated(member, 'subscribe_to_newsletter')
        update_newsletter_subscription(member, event)

    def test_onMemberPropsUpdates_unsubscribe(self):
        portal_state = self.portal.restrictedTraverse('@@plone_portal_state')
        member = portal_state.member()
        member.setProperties(subscribe_to_newsletter=False)
        event = PropertiesUpdated(member, 'subscribe_to_newsletter')
        update_newsletter_subscription(member, event)
    
    
    def test_update_newsletter_subscription(self):
        self.fail()
    
