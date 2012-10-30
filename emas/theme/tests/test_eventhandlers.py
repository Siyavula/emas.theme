import os
import lxml
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName

from base import BaseFunctionalTestCase
from emas.theme.browser.tests.test_practice_service_messages_viewlet import \
    find_viewlet
from emas.theme.interfaces import IEmasThemeLayer

dirname = os.path.dirname(__file__)

class TestEventhandlers(BaseFunctionalTestCase):
    """ Test the intelligent practice messages service viewlets  """
    
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
