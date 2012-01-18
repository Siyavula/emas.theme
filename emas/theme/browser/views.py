import json
from zope.component import queryUtility, getUtility
from zope.app.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue

from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.users.browser.personalpreferences import UserDataPanel
from upfront.shorturl.browser.views import RedirectView

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Archetypes.interfaces import IBaseContent

from emas.theme.behaviors.annotatable import IAnnotatableContent
from emas.theme.interfaces import IEmasSettings
from emas.theme import MessageFactory as _

class EmasSettingsForm(RegistryEditForm):
    schema = IEmasSettings
    label = _(u'EMAS Settings')
    description = _(u"Use the settings below to configure "
                    u"emas.theme for this site")

class EmasControlPanel(ControlPanelFormWrapper):
    form = EmasSettingsForm

class AnnotatorConfigViewlet(ViewletBase):
    """ Adds a bit of javascript to the top of the page with details about
        the annotator. """
    index = ViewPageTemplateFile('annotatorconfig.pt')

    def update(self):
        super(AnnotatorConfigViewlet, self).update()
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(IEmasSettings)

    def accountId(self):
        return self.settings.accountid

    def annotatorStore(self):
        return self.settings.store

    def userId(self):
        return self.portal_state.member().getId()

class AnnotatorHelpViewlet(ViewletBase):
    """ Adds a help panel for the annotator. """
    index = ViewPageTemplateFile('annotatorhelp.pt')


class SearchView(BrowserView):
    """ Combine searching for shortcode and searchabletext
    """

    def __call__(self):
        searchtext = self.request.get('SearchableText')
        shortcodeview = RedirectView(self.context, self.request)
        target = shortcodeview.lookup(searchtext)
        if target:
            self.request.response.redirect(target)
        else:
            state = self.context.restrictedTraverse('@@plone_portal_state')
            root = state.navigation_root()
            search_url = '%s/search?SearchableText=%s' % (
                root.absolute_url(), searchtext)
            self.request.response.redirect(search_url)

class AnnotatorEnabledView(BrowserView):
    """ Return true if annotator should be enabled
    """
    def enabled(self):
        if IAnnotatableContent.providedBy(self.context):
            return IAnnotatableContent(self.context).enableAnnotations
            
        if not IBaseContent.providedBy(self.context):
            return False
        enabled = self.context.Schema().getField(
            'enableAnnotations').getAccessor(self.context)()
        return enabled and bool(self.request.get('HTTP_X_THEME_ENABLED', None))

    __call__ = enabled


class EmasUserDataPanel(UserDataPanel):
    def __init__(self, context, request):
        super(EmasUserDataPanel, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('credits')

class CreditsViewlet(ViewletBase):
    """ Adds a help panel for the annotator. """
    index = ViewPageTemplateFile('credits-viewlet.pt')

    @property
    def credits(self):
        member = self.context.restrictedTraverse(
            '@@plone_portal_state').member()
        return member.getProperty('credits', 0)


class AddQuestionView(BrowserView):
    """ Add a question to the questions folder and associate it with the
        given context.
    """
    def addQuestion(self):
        request = self.request
        context = self.context

        portal = context.restrictedTraverse('@@plone_portal_state').portal()
        questions = portal._getOb('questions')
        id = questions.generateId('question')
        questions.invokeFactory('siyavula.what.question', id=id)
        question = questions._getOb(id)
        question.question = request.get('question')
        
        intids = getUtility(IIntIds)
        try:
            new_id = intids.getId(self.context)
            question.relatedContent = RelationValue(new_id)
            return question
        except:
            raise 'Cannot calculate intid for %s' %self.context.getId()

    def addQuestionJSON(self):
        question = self.addQuestion() 
        message = "Question %s was added" %question.question
        result = 'success'
        return json.dumps({result: result,
                           message: message})
