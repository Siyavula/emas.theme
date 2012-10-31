import os
import lxml
from lxml.etree import ParserError

from zope.interface import alsoProvides 
from zope.viewlet.interfaces import IViewletManager
from zope.component import queryMultiAdapter

from Products.Five.browser import BrowserView as View
from Products.CMFCore.utils import getToolByName

from emas.theme.interfaces import IEmasThemeLayer
from emas.theme import MessageFactory as _

from emas.theme.tests.base import BaseFunctionalTestCase

dirname = os.path.dirname(__file__)

def find_viewlet(context, request, manager_name, viewlet_name, layer=None):
    if layer:
        alsoProvides(request, layer)

    view = View(context, request)
    manager = queryMultiAdapter(
        (context, request, view),
        IViewletManager,
        manager_name,
        default=None
    )
    manager.update()
    viewlets = manager.viewlets
    viewlets = [v for v in viewlets if v.__name__ == viewlet_name]
    return viewlets and viewlets[0] or None


class TestPracticeServiceMessagesViewlet(BaseFunctionalTestCase):
    """ Test the intelligent practice messages service viewlets  """
    
    def setUp(self):
        super(TestPracticeServiceMessagesViewlet, self).setUp()
        self.setRoles(['Reader',])
        self.context = self.portal.maths
        self.request = self.portal.REQUEST
        self.manager_name = 'plone.belowcontenttitle'
        self.themelayer = IEmasThemeLayer
        self.viewlet_name = 'emas.practice_service_messages'

    def test_viewlet_exists(self):
        viewlet = self.get_viewlet()
        self.failUnless(viewlet)
        self.failUnless(viewlet.__name__ == self.viewlet_name)

    def test_no_messages(self):
        viewlet = self.get_viewlet()
        result = viewlet.index()
        self.assertRaises(ParserError, lxml.html.fromstring, result)

    def test_noaccess_message(self):
        plone_utils = getToolByName(self.portal, 'plone_utils')
        message = _(u'You do not currently have access to this service.')
        plone_utils.addPortalMessage(message, 'services-warning')
        
        viewlet = self.get_viewlet()
        result = viewlet.index()

        expected_result = \
u"""\n\n    <dl class="portalMessage services-warning">\n        <dt>Services-warning</dt>\n        <dd>You do not currently have access to this service.</dd>\n    </dl>\n\n\n"""
        self.assertEqual(result, expected_result, 'Incorrect message returned.')

        doc = lxml.html.fromstring(result)
        self.assertEqual(len(doc.xpath('//dl')), 1, 'No content found.')
    
    def get_viewlet(self):
        viewlet = find_viewlet(self.context,
                               self.request,
                               self.manager_name,
                               self.viewlet_name,
                               self.themelayer)
        return viewlet
