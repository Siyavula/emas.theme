import base64
import httplib
import urllib2
import lxml
import logging
from types import ListType
from itertools import chain
from urllib import urlencode
from urlparse import urlparse
from ordereddict import OrderedDict
from datetime import datetime, timedelta

from ZPublisher import NotFound, BadRequest
from zope.interface import Interface, implements, alsoProvides
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID

from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from emas.app.browser.utils import practice_service_uuids
from emas.app.browser.utils import member_services_for_subject
from emas.app.browser.utils import get_subject_from_path, get_grade_from_path

from emas.theme.interfaces import IEmasSettings, IMemberServiceGroup

from emas.theme import MessageFactory as _

log = logging.getLogger('emas.theme.browser.practice')

MONTH = 30
YEAR = 365


class IPractice(Interface):
    """ Marker interface for IPractice """

class IPracticeLayer(IBrowserRequest):
    """ Applied to HTTP request object to customise layout e.g. the
        premium services viewlet should be hidden when we are
        practising.
    """

class Practice(BrowserView):
    """ Proxy for practice in Monassis
    """
    NUM_DAYS = 30

    implements(IPractice, IPublishTraverse)

    index = ViewPageTemplateFile('templates/practice.pt')

    def __init__(self, context, request):
        super(Practice, self).__init__(context, request)
        self.settings = queryUtility(IRegistry).forInterface(IEmasSettings)

    def __call__(self, *args, **kw):
        alsoProvides(self.request, IPracticeLayer)
        
        self.subject = \
            get_subject_from_path('/'.join(self.context.getPhysicalPath()))
        self.memberservices = []
        self.practice_services = []
        self.accessto = ''

        portal_state = self.context.restrictedTraverse('@@plone_portal_state')
        path = self.request.get_header('PATH_INFO')

        member = portal_state.member()
        sm = getSecurityManager()
        self.ismanager = sm.checkPermission(
            permissions.ManagePortal, self.context) or False
        # give managers access to everything
        if self.ismanager:
            self.accessto = ('maths-grade-10,maths-grade-11,maths-grade-12,'
                        'science-grade-10,science-grade-11,science-grade-12')
        elif member.getId():
            self.memberservices, self.practice_services = \
                self.get_services(self.context, member.getId(), self.subject)
            self.accessto = self.get_accessto(self.practice_services)
        else:
            self.accessto = ''

        if portal_state.anonymous():
            memberid = 'Anonymous'
        else:
            memberid = member.getId()
        log.info('X-Access-To for %s: %s' % (memberid, self.accessto))

        urlparts = urlparse(self.settings.practiceurl)
        practiceserver = urlparts.netloc
        
        path = self.request.get_header('PATH_INFO', '')
        if path and len(path) > 0:
            startpos = path.find(self.__name__)
            # strip the view name from the path
            path = path[startpos+len(self.__name__):]

        headers = {
            "Accept-Encoding": "identity",
            "Host": self.request.HTTP_HOST,
            "Connection": "close",
            "Cookie": self.request.HTTP_COOKIE,
            "Referer": self.request.HTTP_REFERER,
            "User-Agent": self.request.HTTP_USER_AGENT,
        }
        if not portal_state.anonymous():
            headers["Authorization"] = 'Basic ' + base64.b64encode(memberid)
            headers["X-Access-To"] = self.accessto

        # Forward GET and POST requests; complain for all other request types
        if self.request.method == 'GET':
            conn = httplib.HTTPConnection(practiceserver)
            conn.request("GET", path, headers=headers)
        elif self.request.method == 'POST':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            conn = httplib.HTTPConnection(practiceserver, timeout=10)
            conn.request("POST", path,
                         body=urlencode(self.request.form.items()),
                         headers=headers)
        else:
            return self.request.RESPONSE.unauthorized()
        
        self.html = ''
        # Handle response from Monassis server
        response = conn.getresponse()

        # Force no caching of response
        self.request.RESPONSE.appendHeader('Cache-Control',
                                           'no-store, no-cache')

        if response.status == 200:   # Ok
            body = response.read()
            if response.msg.type == 'text/html':
                html = lxml.html.fromstring(body)
                html.make_links_absolute(base_url=self.settings.practiceurl,
                                         resolve_base_href=True)
                content = html.find('.//*[@id="content"]')
                if content is not None:
                    self.html = lxml.html.tostring(content)
                else:
                    self.html = body

                return self.index()
            else:
                resp = self.request.RESPONSE
                for key in ['Content-Length', 'Content-Type', 'Content-Disposition']:
                    value = response.msg.get(key)
                    if value is not None:
                        resp.setHeader(key, value)
                resp.write(body)

        elif response.status == 302: # Found
            urlparts = urlparse(response.msg.get('location'))
            redirto = '%s%s' % (self.context.absolute_url(), urlparts.path)
            if urlparts.fragment:
                redirto += '#%s' % urlparts.fragment
            return self.request.RESPONSE.redirect(redirto)
        elif response.status == 400: # Bad request
            raise BadRequest('The URL:%s is a bad request.' %path)
        elif response.status == 403: # Forbidden
            if portal_state.anonymous():
                return self.request.RESPONSE.unauthorized()
            else:
                log.info('User:%s not allowed to access URL:%s.' % 
                    (memberid, path))
                self.add_noaccess_message()
                return self.index()
        elif response.status == 404: # NotFound
            raise NotFound('The URL:%s could not be found.' %path)
        else:
            log.warn('Upstream returned:%s for URL:%s. Status is not handled.' %
                (response.status, path))
    
    def add_first_login_message(self, member):
        last_login_time = member.getProperty('last_login_time')
        login_time = member.getProperty('login_time')
        # if it last login and current login are within 2 seconds of eachother, 
        # we consider this the 'first login'
        if login_time.micros() - last_login_time.micros() < 2000000:
            plone_utils = getToolByName(self.context, 'plone_utils')
            message = _(u'Have a look at the practice services.')
            plone_utils.addPortalMessage(message, 'info')
        
    def services_active(self):
        """ If the user has the ManagePortal permission.
            OR
            If the user has any active services.
            We want to display the practice service content.
        """
        return self.ismanager or len(self.memberservices) > 0
    
    def get_days_to_expiry_date(self):
        """ Sort member services according to expiry date,
            closest to expiry first.
            Then return the difference in days, between 'now'
            and the member service expiry date.
            This is naive, since the member services potentially all have
            different expiry dates.

            TODO:
            Update the design in conjunction with the Siyavula team.
        """
        path = self.request.get_header('PATH_INFO', '')
        subject = get_subject_from_path(path)
        grade = get_grade_from_path(path)

        days = self.settings.annual_expiry_warning_threshold
        now = datetime.now().date()

        for ms in self.filtered(self.memberservices, subject, grade):
            delta = (ms.expiry_date - now).days
            if delta < days:
                days = delta
        return days

    def filtered(self, memberservices, subject, grade):
        # Short circuit the filtering here. If we don't have a subject, we
        # cannot filter properly.
        if  subject == None:
            return memberservices

        filteredms = []
        for ms in memberservices:
            service = ms.related_service.to_object
            if service.subject == subject:
                # if we don't have a grade, we want to return this memberservice
                if not grade:
                    filteredms.append(ms)
                # if we have a grade, check it
                elif service.grade == grade:
                    filteredms.append(ms)
                
        return filteredms 
        
    def practice_service_messages(self):
        grades = [10, 11, 12]
        messages = []

        expiring_services = self.expiring_services()
        # Format messages about expiring services.
        if expiring_services.values():
            msg = ''
            num_days = self.number_of_days_until(expiring_services)
            days = num_days > 1 and 'days.' or 'day.'
            template = 'Your access to %s practice will expire in %s '+days

            service_grades = expiring_services.keys()
            service_grades.sort()
            if service_grades == grades:
                msg = template % (self.subject.capitalize(), num_days)
            else:
                services = ' and '.join(['Grade %s' %s for s in service_grades])
                msg = template % (services, num_days)
            messages.append(msg)
        else:
            # no services expiring? Then don't show any messages.
            return []
        
        # Now, we do the formatting of the active services.
        active_services = self.active_services()
        # Remove all the services that we already reported on above.
        for grade in expiring_services.keys():
            active_services.pop(grade, None)
        if active_services.values():
            # flatten the list of memberservice lists
            memberservices = ListType(chain.from_iterable(active_services.values()))
            # sort according to expiry_date
            memberservices.sort(key=lambda service: service.expiry_date)
            # use the last expiry date
            formatted_expiry_date = \
                self.format_date(memberservices[-1].expiry_date)

            msg = ''
            template = 'You will still have access to %s practice until %s.'
            service_grades = active_services.keys()
            service_grades.sort()
            services = ' and '.join(['Grade %s' %s for s in service_grades])
            msg = template % (services, formatted_expiry_date) 
            messages.append(msg)
        
        # Lastly, add a link to the order form.
        if expiring_services:
            messages.append(
                '<a href="/order">To extend your subscription, click here.</a>')

        return messages

    def format_date(self, expiry_date):
        if expiry_date.year == datetime.now().year:
            return expiry_date.strftime("%e %B")
        return expiry_date.strftime("%e %B %Y")

    def number_of_days_until(self, expiring_services):
        # flatten the list of memberservice lists
        memberservices = ListType(chain.from_iterable(expiring_services.values()))
        # sort according to expiry_date
        memberservices.sort(key=lambda service: service.expiry_date)
        # use the last expiry date
        expiry_date = memberservices[0].expiry_date
        now = datetime.now().date()
        delta = expiry_date - now
        return delta.days
        
    def expiring_services(self):
        now = datetime.now()
        expiring_services = {}
        for ms in self.memberservices:
            if self.is_expiring(now, ms):
                grade = int(ms.related_service.to_object.grade.split('-')[-1])
                tmpservices = expiring_services.get(grade, [])
                tmpservices.append(ms)
                expiring_services[grade] = tmpservices
        return expiring_services
    
    def active_services(self):
        now = datetime.now()
        active_services = {}
        for ms in self.memberservices:
            if not self.is_expiring(now, ms):
                grade = int(ms.related_service.to_object.grade.split('-')[-1])
                tmpservices = active_services.get(grade, [])
                tmpservices.append(ms)
                active_services[grade] = tmpservices
        return active_services
    
    def is_expiring(self, cutoff_date, memberservice):
        days = self.memberservice_expiry_threshold(memberservice)
        expiry_threshold = (cutoff_date + timedelta(days)).date()
        if memberservice.expiry_date <= expiry_threshold:
            return True
        return False
    
    def memberservice_expiry_threshold(self, memberservice):
        """ This method helps us decide when to show expiry warnings.

            For all services that have subscription_period of a YEAR or less,
            but not less than a MONTH, we want to show the message within the,
            'annual_expiry_warning_threshold'.

            For all services that have subscription_period of a MONTH or less,
            we want to show the message within the,
            'monthly_expiry_warning_threshold'. 
        """
        subperiod = memberservice.related_service.to_object.subscription_period
        if subperiod <= MONTH:
            return self.settings.monthly_expiry_warning_threshold
        elif subperiod <= YEAR:
            return self.settings.annual_expiry_warning_threshold

    def get_services(self, context, userid, subject):
        memberservices = []
        services = []

        service_uuids = practice_service_uuids(self.context)
        tmpservices = member_services_for_subject(self.context,
                                                  service_uuids,
                                                  userid,
                                                  subject)
        for ms in tmpservices:
            service = ms.related_service.to_object
            if '@@practice' in service.access_path:
                memberservices.append(ms)
                services.append(service)
        return memberservices, services

    def get_accessto(self, practice_services):
        accessto = ','.join(
            ['%s-%s' %(s.subject, s.grade) for s in practice_services]
        )
        return accessto

    def add_noaccess_message(self):
        # set a portal message
        plone_utils = getToolByName(self.context, 'plone_utils')
        message = _(u'You do not currently have access to this service.')
        plone_utils.addPortalMessage(message, 'info')
        return message

    def publishTraverse(self, request, name):
        """ consume the subpath """
        path = request['TraversalRequestNameStack']
        subpath = path[:]
        path[:] = []
        subpath.reverse()
        request.set('traverse_subpath', subpath)
        return self
