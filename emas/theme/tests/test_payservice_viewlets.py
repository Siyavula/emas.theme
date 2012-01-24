import os
import unittest2 as unittest
from base import INTEGRATION_TESTING

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView as View
from zope.interface import alsoProvides 
from zope.viewlet.interfaces import IViewletManager
from zope.component import queryMultiAdapter

from emas.theme.interfaces import IEmasThemeLayer

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


class TestRegisterToAskQuestionsViewlet(unittest.TestCase):
    """ Test the pay service viewlets  """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.context = self.portal
        self.request = self.portal.REQUEST
    
    def _get_viewlet(self):
        manager_name = 'plone.belowcontent'
        viewlet_name = 'register-to-ask-questions'
        layer = IEmasThemeLayer 
        viewlet = find_viewlet(self.context,
                               self.request,
                               manager_name,
                               viewlet_name, layer)
        return viewlet

    def test_viewlet_exists(self):
        viewlet = self._get_viewlet() 
        self.failUnless(viewlet, 'Viewlet does not exist.')

    def test_has_credits(self):
        viewlet = self._get_viewlet() 

        self.assertEqual(viewlet.has_credits, False)

        pmt = getToolByName(self.context, 'portal_membership')
        member = pmt.getAuthenticatedMember()
        member.setMemberProperties({'credits': 100})

        self.assertEqual(viewlet.has_credits, True)
    
    def test_is_registered(self):
        viewlet = self._get_viewlet()
        viewlet.update()

        self.assertEqual(
            viewlet.is_registered, False)
        
        self.request.form["emas.theme.registertoaskquestions.submitted"] = 'submitted'
        self.request.form["registertoaskquestions"] = "on"
        viewlet.update()

        self.assertEqual(
            viewlet.is_registered, True)

    def test_rendering(self):
        viewlet = self._get_viewlet()
        viewlet.update()

        html = viewlet.render().encode('utf-8')
        file = open(os.path.join(
            dirname, 'data', 'no_credits.html'))
        reference_html = file.read()
        file.close()

        self.assertEqual(html, reference_html)
        
        self.request.form["emas.theme.registertoaskquestions.submitted"] = 'submitted'
        self.request.form["registertoaskquestions"] = "on"
        pmt = getToolByName(self.context, 'portal_membership')
        member = pmt.getAuthenticatedMember()
        member.setMemberProperties({'credits': 100})
        viewlet.update()
        html = viewlet.render().encode('utf-8')

        file = open(os.path.join(
            dirname, 'data', 'register.html'))
        reference_html = file.read()
        file.close()

        self.assertEqual(html, reference_html)
