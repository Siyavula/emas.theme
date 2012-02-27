import os
import unittest2 as unittest
from base import INTEGRATION_TESTING

from Products.CMFCore.permissions import ModifyPortalContent
from Products.ATContentTypes.content.folder import ATFolder
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView as View
from zope.interface import alsoProvides 
from zope.viewlet.interfaces import IViewletManager
from zope.component import queryMultiAdapter, queryUtility

from emas.theme.browser.views import NULLDATE
from emas.theme.interfaces import IEmasThemeLayer, IEmasServiceCost
from siyavula.what.interfaces import ISiyavulaWhatLayer

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


class TestPayserviceViewletBase(unittest.TestCase):
    """ Test the pay service viewlets  """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        pps = self.portal.restrictedTraverse('@@plone_portal_state')
        member = pps.member()
        memberid = member.getId()
        folder = ATFolder(memberid)
        transactions = self.portal.transactions
        transactions._setObject(memberid, folder)
        transactions.reindexObject()
        # Finally, change its permissions
        folder.manage_permission(ModifyPortalContent, roles=[], acquire=0)
        # Make sure the user's service registration dates are correct
        properties = {'askanexpert_registrationdate': NULLDATE,
                      'answerdatabase_registrationdate': NULLDATE,
                      'moreexercise_registrationdate': NULLDATE,
                     }
        member.setProperties(properties)

        self.context = self.portal.maths
        self.context.allowQuestions = True
        self.request = self.portal.REQUEST
        self.manager_name = 'plone.belowcontent'
        self.themelayer = IEmasThemeLayer 

        self.viewlet_name = None 
        self.formsubmit_token = None
        self.formfield = None
        self.memberproperty = None
        self.creditproperty = ''

    def _get_viewlet(self):
        viewlet = find_viewlet(self.context,
                               self.request,
                               self.manager_name,
                               self.viewlet_name,
                               self.themelayer)
        return viewlet

    def _test_viewlet_exists(self):
        viewlet = self._get_viewlet() 
        self.failUnless(viewlet, 'Viewlet does not exist.')

    def _test_has_credits(self):
        viewlet = self._get_viewlet() 

        self.assertEqual(viewlet.has_credits, False)

        pmt = getToolByName(self.context, 'portal_membership')
        member = pmt.getAuthenticatedMember()
        member.setMemberProperties({'credits': 100})

        self.assertEqual(viewlet.has_credits, True)
    
    def _test_is_registered(self):
        viewlet = self._get_viewlet()
        viewlet.update()

        self.assertEqual(
            viewlet.is_registered, False)
        
        view = self.portal.restrictedTraverse('@@emas-transaction')
        view.buyCredit(1000, "Credits purchased")

        self.request.form[self.formsubmit_token] = 'submitted'
        self.request.form[self.formfield] = "on"
        self.request.form['form.button.submit'] = 'Register'
        viewlet.update()

        self.assertEqual(
            viewlet.is_registered, True)

    def _test_rendering(self, nocredits_name, not_registered_name, registered_name):
        viewlet = self._get_viewlet()
        viewlet.update()
        
        # not enough credits test
        html = viewlet.render().encode('utf-8')
        file = open(os.path.join(
            dirname, 'data', nocredits_name))
        reference_html = file.read()
        file.close()

        self.assertEqual(html, reference_html)
        
        #test for enough credits, but not registered yet
        self.request.form[self.formsubmit_token] = 'submitted'
        self.request.form[self.formfield] = "on"
        pmt = getToolByName(self.context, 'portal_membership')
        member = pmt.getAuthenticatedMember()
        member.setMemberProperties({'credits': 100})
        viewlet.update()
        html = viewlet.render().encode('utf-8')

        file = open(os.path.join(
            dirname, 'data', not_registered_name))
        reference_html = file.read()
        file.close()

        self.assertEqual(html, reference_html)
        
        # enough credits and registered
        self.request.form[self.formsubmit_token] = 'submitted'
        self.request.form[self.formfield] = "on"
        self.request.form['form.button.submit'] = 'Register'
        viewlet.update()
        html = viewlet.render().encode('utf-8')
        
        file = open(os.path.join(
            dirname, 'data', registered_name))
        reference_html = file.read()
        file.close()

        self.assertEqual(html, reference_html)


class TestRegisterToAskQuestionsViewlet(TestPayserviceViewletBase):
    """ Test the pay service viewlets  """

    def setUp(self):
        super(TestRegisterToAskQuestionsViewlet, self).setUp()
        self.viewlet_name = 'register-to-ask-questions'
        self.formsubmit_token = 'emas.theme.registertoaskquestions.submitted'
        self.formfield = 'registertoaskquestions'
        self.memberproperty = 'askanexpert_registrationdate'
        self.creditproperty = 'questionCost'
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IEmasServiceCost)
        setattr(settings, self.creditproperty, 100)
    
    def test_viewlet_exists(self):
        self._test_viewlet_exists()

    def test_has_credits(self):
        self._test_has_credits()

    def test_is_registered(self):
        self._test_is_registered()

    def test_rendering(self):
        self._test_rendering('askquestion_nocredit.html',
                             'askquestion_not_registered.html',
                             'askquestion_registered.html')


class TestRegisterToAccessAnswerDatabaseViewlet(TestPayserviceViewletBase):
    """ Test the pay service viewlets  """

    def setUp(self):
        super(TestRegisterToAccessAnswerDatabaseViewlet, self).setUp()
        self.viewlet_name = 'register-to-access-answers'
        self.formsubmit_token = 'emas.theme.registertoaccessanswerdatabase.submitted'
        self.formfield = 'registertoaccessanswerdatabase'
        self.memberproperty = 'answerdatabase_registrationdate'
        self.creditproperty = 'answerCost'
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IEmasServiceCost)
        setattr(settings, self.creditproperty, 100)
    
    def test_viewlet_exists(self):
        self._test_viewlet_exists()

    def test_has_credits(self):
        self._test_has_credits()

    def test_is_registered(self):
        self._test_is_registered()

    def test_rendering(self):
        self._test_rendering('accessanswers_nocredit.html',
                             'accessanswers_not_registered.html',
                             'accessanswers_registered.html')


class TestRegisterForMoreExerciseViewlet(TestPayserviceViewletBase):
    """ Test the pay service viewlets  """

    def setUp(self):
        super(TestRegisterForMoreExerciseViewlet, self).setUp()
        self.viewlet_name = 'register-for-more-exercise'
        self.formsubmit_token = 'emas.theme.registerformoreexercise.submitted'
        self.formfield = 'registerformoreexercise'
        self.memberproperty = 'moreexercise_registrationdate'
        self.creditproperty = 'exerciseCost'
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IEmasServiceCost)
        setattr(settings, self.creditproperty, 100)
    
    def test_viewlet_exists(self):
        self._test_viewlet_exists()

    def test_has_credits(self):
        self._test_has_credits()

    def test_is_registered(self):
        self._test_is_registered()

    def test_rendering(self):
        self._test_rendering('moreexercise_nocredit.html',
                             'moreexercise_not_registered.html',
                             'moreexercise_registered.html')

class TestQuestionAddViewlet(TestPayserviceViewletBase):
    
    def setUp(self):
        super(TestQuestionAddViewlet, self).setUp()
        self.viewlet_name = 'question-add'

    def test_viewlet_exists(self):
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'question-add'
        themelayer = ISiyavulaWhatLayer
        viewlet = find_viewlet(context,
                               self.request,
                               manager_name,
                               viewlet_name,
                               themelayer)
