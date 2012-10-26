import base64
import httplib
import urllib2
import lxml
import logging
from urllib import urlencode
from urlparse import urlparse

from zope.interface import Interface, implements, alsoProvides
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from emas.app.browser.utils import practice_service_uuids
from emas.app.browser.utils import member_services 

from emas.theme.interfaces import IEmasSettings

from emas.theme import MessageFactory as _

log = logging.getLogger('emas.theme.browser.practice')

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

    implements(IPractice, IPublishTraverse)

    index = ViewPageTemplateFile('templates/practice.pt')

    def __call__(self, *args, **kw):
        alsoProvides(self.request, IPracticeLayer)
        self.service_expired = False

        portal_state = self.context.restrictedTraverse('@@plone_portal_state')
        if portal_state.anonymous():
            self.add_message()
            self.html = "Order intelligent practice now."
            return self.index()

        member = portal_state.member()
        sm = getSecurityManager()
        # give managers access to everything
        if sm.checkPermission(permissions.ManagePortal, self.context):
            accessto = ('maths-grade-10,maths-grade-11,maths-grade-12,'
                        'science-grade-10,science-grade-11,science-grade-12')
        elif member.getId():
            service_uuids = practice_service_uuids(self.context)
            memberservices = member_services(self.context, service_uuids)
            services = [ms.related_service.to_object for ms in memberservices]
            services = [service for service in services if '@@practice' in service.access_path]
            accessto = ','.join(
                ['%s-%s' %(s.subject, s.grade) for s in services]
            )
        else:
            accessto = ''
        memberid = member.getId() or 'Anonymous'

        log.info('X-Access-To for %s: %s' % (memberid, accessto))

        settings = queryUtility(IRegistry).forInterface(IEmasSettings)
        urlparts = urlparse(settings.practiceurl)
        practiceserver = urlparts.netloc
        
        path = self.request.get_header('PATH_INFO')
        startpos = path.find(self.__name__)
        # strip the view name from the path
        path = path[startpos+len(self.__name__):]

        headers = {
            "Accept-Encoding": "identity",
            "Host": self.request.HTTP_HOST,
            "Connection": "close",
            "Authorization": 'Basic ' + base64.b64encode(memberid),
            "Cookie": self.request.HTTP_COOKIE,
            "X-Access-To": accessto,
            "Referer": self.request.HTTP_REFERER,
        }

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

        # Handle response from Monassis server
        response = conn.getresponse()
        if response.status == 200:   # Ok
            body = response.read()
            if response.msg.type == 'text/html':
                html = lxml.html.fromstring(body)
                html.make_links_absolute(base_url=settings.practiceurl,
                                         resolve_base_href=True)
                content = html.find('.//*[@id="content"]')
                if content is not None:
                    self.html = lxml.html.tostring(content)
                else:
                    self.html = body

                return self.index()
            else:
                resp = self.request.RESPONSE
                resp.setHeader('Content-Type', response.msg.type)
                resp.setHeader('Content-Length',
                               response.msg.get('content-length'))
                resp.write(body)

        elif response.status == 302: # Found
            urlparts = urlparse(response.msg.get('location'))
            redirto = '%s%s' % (self.context.absolute_url(), urlparts.path)
            if urlparts.fragment:
                redirto += '#%s' % urlparts.fragment
            return self.request.RESPONSE.redirect(redirto)
        else:
            self.html = "Order intelligent practice now."
            self.add_message()
            return self.index()

    def add_message(self):
        # set a portal message
        self.service_expired = True
        plone_utils = getToolByName(self.context, 'plone_utils')
        message = _(u'You do not currently have access to this service.')
        plone_utils.addPortalMessage(message)
        return message

    def publishTraverse(self, request, name):
        """ consume the subpath """
        path = request['TraversalRequestNameStack']
        subpath = path[:]
        path[:] = []
        subpath.reverse()
        request.set('traverse_subpath', subpath)
        return self
