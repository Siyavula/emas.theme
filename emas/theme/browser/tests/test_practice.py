import lxml
import transaction
from datetime import date
import unittest2 as unittest
from DateTime import DateTime
from browserbase import BaseFunctionalTestCase

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

class TestPracticeBrowserView(BaseFunctionalTestCase):
    
    def afterSetUp(self):
        settings = queryUtility(IRegistry).forInterface(IEmasSettings)
        settings.practiceurl = u'http://localhost:37183'
        
    def test_not_logged_in(self):
        self.logout()
        view = self.portal.restrictedTraverse('@@practice')
        self.assertRaises(Unauthorized, view,
                         'The system should force a login.')

    def test_logged_in_not_active(self):
        self.deactivate_services()

        view = self.portal.restrictedTraverse('@@practice')
        self.update_request(view) 
        result = view()

        self.assertGreater(len(result), 0,
                           'No result found.')
        self.assertEqual(view.services_active(), False,
                         'The service should not be active.')
        doc = lxml.html.fromstring(result)
        elements = doc.xpath('//a[contains(.,"orders")]')
        self.assertGreater(len(elements), 0,
                           'No order links found.')

    def test_logged_in_not_expired(self):
        view = self.portal.restrictedTraverse('@@practice')
        self.update_request(view)
        result = view()

        self.assertEqual(view.services_active(), True,
                         'The service should be active.')
        doc = lxml.html.fromstring(result)
        elements = doc.xpath('//a[contains(.,"orders")]')
        self.assertEqual(len(elements), 0,
                           'There should be no order links.')
    
    def test_logged_in_grade10_maths(self):
        view = self.portal.restrictedTraverse('@@practice')
        self.update_request(view)
        result = view()

        assert 'maths-grade-10' in view.accessto, \
               'Grade 10 Maths service not in memberservices.'
    
    def test_practice_service_info_on_first_login(self):
        portal_state = self.portal.restrictedTraverse('@@plone_portal_state')
        member = portal_state.member()
        default = DateTime('2000/01/01')
        member.setProperties(login_time=default,
                             last_login_time=default)

        view = self.portal.restrictedTraverse('@@practice')
        self.update_request(view)
        # The call to loginUser is the one that fires the required event.
        # The testcase's login method simly creates a new security manager, it
        # does not lead to the IUserLoggedInEvent. 
        self.portal.portal_membership.loginUser(view.request)
        result = view()
        doc = lxml.html.fromstring(result)
        elements = doc.xpath('//a[contains(.,"@@practice")]')
        self.assertEqual(len(elements), 0,
                         'No link to @@practice found.')
    
    def test_expiry_warning(self):
        view = self.portal.restrictedTraverse('@@practice')
        self.update_request(view)
        result = view()
        self.assertEqual(view.show_expirywarning(), True,
                         'Trial service should all expire withing 30 days.')

    def test_get_services(self):
        view = self.portal.restrictedTraverse('@@practice')
        self.update_request(view)
        result = view()

        self.assertEqual(len(view.memberservices), 6,
                         'There should be 6 practice memberservices.')

        for ms in view.memberservices:
            assert (IMemberService.providedBy(ms),
                'The memberservice does not provide the correct interface.')

        for service in view.practice_services:
            assert (IService.providedBy(service),
                'The practice_service does not provide the correct interface.')

    def deactivate_services(self):
        memberservices = self.portal._getOb('memberservices')
        expired = date(1970, 01, 01)
        for service in memberservices.objectValues():
            service.expiry_date = expired
            service.reindexObject(idxs=['expiry_date'])

    def create_memberservices(self, userid, services):
        self.logout()
        self.loginAsPortalOwner()
        
        products_and_services = self.portal._getOb('products_and_services')
        memberservices = self.portal._getOb('memberservices')
        for service in services:
            service = products_and_services._getOb(service)
            mstitle = '%s for %s' % (service.title, userid)
            related_service = create_relation(service.getPhysicalPath())

            props = {'title': mstitle,
                     'userid': userid,
                     'related_service': related_service,
                     'service_type': service.service_type
                     }


            ms = createContentInContainer(
                memberservices,
                'emas.app.memberservice',
                False,
                **props
            )
            
            self.login()

    def update_request(self, view):
        cookie = ''
        path = '/emas/maths/@@practice/grade-10'
        host = 'localhost:8080'
        serverurl = 'http://%s' % host
        referer = '%s%s' % (serverurl, path)
        props = {'method':             'GET',
                 'PATH_INFO':          path,
                 'HTTP_HOST':          host,
                 'HTTP_COOKIE':        cookie,
                 'HTTP_REFERER':       referer,
                 'SERVER_URL':         serverurl,
                 'CONTENT_LENGTH':     '0',
                 'GATEWAY_INTERFACE':  'TestFooInterface/1.0',}

        for k, v in props.items():
            setattr(view.request, k, v)
        
        return view.request


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPracticeBrowserView))
    return suite
