import base64
import httplib
import urllib2
import lxml
from urllib import urlencode
from urlparse import urlparse

from zope.interface import Interface, implements
from zope.publisher.interfaces import IPublishTraverse
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from emas.theme.interfaces import IEmasSettings

class IPractice(Interface):
    """ Marker interface for IPractice """

class Practice(BrowserView):
    """ Proxy for practice in Monassis
    """

    implements(IPractice, IPublishTraverse)

    index = ViewPageTemplateFile('templates/practice.pt')

    def __call__(self, *args, **kw):
        portal_state = self.context.restrictedTraverse('@@plone_portal_state')
        if portal_state.anonymous() and \
                self.request.REMOTE_ADDR not in ('127.0.0.1', 'localhost'):
            return self.request.RESPONSE.unauthorized()

        member = portal_state.member()
        memberid = member.getId() or 'Anonymous'

        settings = queryUtility(IRegistry).forInterface(IEmasSettings)
        urlparts = urlparse(settings.practiceurl)
        practiceserver = urlparts.netloc
        
        path = self.request.get_header('PATH_INFO')
        hostroot = path.split(self.__name__)[0] + self.__name__
        path = path.split(self.__name__)[-1]
        url = "%s%s" % (practiceserver, path)

        headers = {
            "Accept-Encoding": "identity",
            "Host": self.request.HTTP_HOST,
            "Connection": "close",
            "Authorization": 'Basic ' + base64.b64encode(memberid),
            "Cookie": self.request.HTTP_COOKIE,
        }

        # Forward GET and POST requests; complain for all other request types
        if self.request.method == 'GET':
            conn = httplib.HTTPConnection(practiceserver)
            conn.request("GET", path, headers=headers)
        elif self.request.method == 'POST':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            conn = httplib.HTTPConnection(practiceserver)
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
            return self.request.RESPONSE.redirect(redirto)
        else:
            return self.request.RESPONSE.unauthorized()


    def publishTraverse(self, request, name):
        """ consume the subpath """
        path = request['TraversalRequestNameStack']
        subpath = path[:]
        path[:] = []
        subpath.reverse()
        request.set('traverse_subpath', subpath)
        return self
