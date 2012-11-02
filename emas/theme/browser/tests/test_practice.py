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
from emas.theme.browser.practice import NUM_DAYS

NUM_SERVICES = 6

class TestPracticeBrowserView(BaseFunctionalTestCase):
    
    def setUp(self):
        super(TestPracticeBrowserView, self).setUp()
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
                         'Trial service should all expire withing NUM_DAYS days.')

    def test_expiry_warning_for_manager(self):
        self.setRoles(('Manager',))
        view = self.portal.restrictedTraverse('@@practice')
        self.update_request(view)
        result = view()
        self.assertEqual(view.show_expirywarning(), False,
                         "We don't show expiry warnings to manager users.")

    def test_get_services(self):
        view = self.portal.restrictedTraverse('@@practice')
        self.update_request(view)
        result = view()

        self.assertEqual(len(view.memberservices), NUM_SERVICES,
                         'There should be %s practice memberservices.')

        for ms in view.memberservices:
            assert (IMemberService.providedBy(ms),
                'The memberservice does not provide the correct interface.')

        for service in view.practice_services:
            assert (IService.providedBy(service),
                'The practice_service does not provide the correct interface.')

    def test_get_services_with_empty_access_path(self):
        view = self.portal.restrictedTraverse('@@practice')
        memberservices, services = view.get_services(self.portal)

        self.assertEqual(len(memberservices), NUM_SERVICES,
                         'There should be %s memberservices.' % NUM_SERVICES)

        self.assertEqual(len(services), NUM_SERVICES,
                         'There should be %s practice services.' % NUM_SERVICES)

        self.clear_access_path()

        memberservices, services = view.get_services(self.portal)

        self.assertEqual(len(memberservices), 0,
                         'There should be 0 memberservices.')

        self.assertEqual(len(services), 0,
                         'There should be 0 practice services.')
    
    def test_filtered_services_for_maths_grade10(self):
        view = self.portal.restrictedTraverse('@@practice')
        self.update_request(view)
        view()

        memberservices, services = view.get_services(self.portal)
        filteredservices = view.filtered(memberservices, 'maths', 'grade-10')
        
        self.assertEqual(len(filteredservices), 1,
                         'There can be onle one!')

    def test_filtered_services_for_maths(self):
        view = self.portal.restrictedTraverse('@@practice')
        self.update_request(view)
        view()

        memberservices, services = view.get_services(self.portal)
        filteredservices = view.filtered(memberservices, 'maths', None)
        
        self.assertEqual(len(filteredservices), 3,
                         'We should find 3  member services for maths.')

    def test_filtered_services_for_None_subject_None_grade(self):
        view = self.portal.restrictedTraverse('@@practice')
        self.update_request(view)
        view()

        memberservices, services = view.get_services(self.portal)
        filteredservices = view.filtered(memberservices, None, None)
        self.assertEqual(len(filteredservices), 6,
                         'We should find 6 member services.')

    def test_manager_user_access(self):
        self.setRoles(('Manager',))
        self.deactivate_services()
        view = self.portal.maths.restrictedTraverse('@@practice')
        self.update_request(view)
        view()
        
        self.assertEqual(len(view.memberservices), 0,
                         'All member services should be expired.')

        self.assertEqual(len(view.accessto.split(',')), NUM_SERVICES,
                         '"accesto" should be %s long.' % NUM_SERVICES)
        
        self.assertEqual(view.services_active(), True,
                         'Manager always has access.')
    
    def test_days_to_expiry_date_calculation(self):
        view = self.portal.restrictedTraverse('@@practice')
        self.update_request(view)
        view()
        
        numdays = NUM_DAYS
        for offset in [0, 10, 10]:
            numdays = numdays - offset
            print 'Testing %s days.' % numdays
            self.change_service_expiry_date(view, offset)
            self.assertEqual(view.get_days_to_expiry_date(), numdays,
                             'Expiry date should be %s days away.' % numdays)
    
    def test_subject_and_grade_computing_no_subject_no_grade(self):
        view = self.portal.restrictedTraverse('@@practice')
        view()
        self.assertEqual(view.get_days_to_expiry_date(), NUM_DAYS,
                         'Expiry date should be %s days away.' % NUM_DAYS)

    def clear_access_path(self):
        memberservices = self.portal._getOb('memberservices')
        for ms in memberservices.objectValues():
            ms.related_service.to_object.access_path = u''

    def change_service_expiry_date(self, view, days):
        for service in view.memberservices:
            newdate = service.expiry_date - timedelta(days)
            service.expiry_date = newdate
            service.reindexObject(idxs=['expiry_date'])

    def deactivate_services(self):
        memberservices = self.portal._getOb('memberservices')
        expired = date(1970, 01, 01)
        for service in memberservices.objectValues():
            service.expiry_date = expired
            service.reindexObject(idxs=['expiry_date'])

    def update_request(self, view):
        cookie = ''
        path = '/emas/maths/@@practice/grade-10'
        host = 'localhost:8080'
        serverurl = 'http://%s' % host
        referer = '%s%s' % (serverurl, path)
        props = {'REQUEST_METHOD':    'GET',
                 'PATH_INFO':          path,
                 'HTTP_HOST':          host,
                 'HTTP_COOKIE':        cookie,
                 'HTTP_REFERER':       referer,
                 'SERVER_URL':         serverurl,
                 'CONTENT_LENGTH':     '0',
                 'GATEWAY_INTERFACE':  'TestFooInterface/1.0',}
        
        view.request.environ.update(props)
        return view.request


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPracticeBrowserView))
    return suite
