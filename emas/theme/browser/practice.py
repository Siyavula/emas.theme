import base64
import urllib2
import lxml
from urllib import urlencode

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
        settings = queryUtility(IRegistry).forInterface(IEmasSettings)

        path = self.request.get_header('PATH_INFO')
        hostroot = path.split(self.__name__)[0] + self.__name__
        path = path.split(self.__name__)[-1]
        url = "%s%s" % (settings.practiceurl, path)

        # Example of virtual hosting url format for Zope
        #
        # hostroot = path.lstrip('/').split(self.__name__)[0] + self.__name__
        # hostroot = '/'.join(['_vh_%s' % part for part in hostroot.split('/')])
        # url = "%s/VirtualHostBase/http/%s/VirtualHostRoot/%s/%s" % (
        #    settings.practiceurl, self.request.HTTP_HOST, hostroot, path)
        member = self.context.restrictedTraverse('@@plone_portal_state'
                                                 ).member() 
        request = urllib2.Request(url)
        userpw = base64.encodestring('%s:%s' % (member.getId(), 'none'))
        request.add_header('Authorization', 'Basic %s' % userpw)

        # Pyramid specific header for Virtual Root
        # request.add_header('X-Vhm-Root', hostroot)
        request.add_header('Host', self.request.HTTP_HOST)
        if self.request.method == 'POST':
            request.add_data(urlencode(self.request.form.items()))
        response = urllib2.urlopen(request)
        content = response.read()
        if response.headers.type == 'text/html':
            html = lxml.html.fromstring(content)
            html.make_links_absolute(base_url=settings.practiceurl,
                                     resolve_base_href=True)
            content = html.find('.//*[@id="content"]')
            if content is not None:
                self.html = lxml.html.tostring(content)
            else:
                self.html = lxml.html.tostring(html)

            return self.index()
        else:
            resp = self.request.RESPONSE
            resp.setHeader('Content-Type', response.headers.type)
            resp.setHeader('Content-Length',
                           response.headers.get('content-length'))
            resp.write(content)


    def publishTraverse(self, request, name):
        """ consume the subpath """
        path = request['TraversalRequestNameStack']
        subpath = path[:]
        path[:] = []
        subpath.reverse()
        request.set('traverse_subpath', subpath)
        return self
