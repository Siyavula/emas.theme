from zope.component import queryUtility

from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.users.browser.personalpreferences import UserDataPanel
from upfront.shorturl.browser.views import RedirectView

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Archetypes.interfaces import IBaseContent
from Products.statusmessages.interfaces import IStatusMessage

from emas.theme.behaviors.annotatable import IAnnotatableContent
from emas.theme.interfaces import IEmasSettings, IEmasServiceCost
from emas.theme import MessageFactory as _

class EmasSettingsForm(RegistryEditForm):
    schema = IEmasSettings
    label = _(u'EMAS Settings')
    description = _(u"Use the settings below to configure "
                    u"emas.theme for this site")

class EmasControlPanel(ControlPanelFormWrapper):
    form = EmasSettingsForm


class EmasServiceCostsForm(RegistryEditForm):
    schema = IEmasServiceCost
    label = _(u'EMAS Service Cost')
    description = _(u"Configure the credit cost"
                    u" of the pay services.")
    
    def updateFields(self):
        super(EmasServiceCostsForm, self).updateFields()
    
    def updateWidgets(self):
        super(EmasServiceCostsForm, self).updateWidgets()

class EmasServiceCostControlPanel(ControlPanelFormWrapper):
    form = EmasServiceCostsForm

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
        self.form_fields = self.form_fields.omit('askanexpert_registrationdate')
        self.form_fields = self.form_fields.omit('answerdatabase_registrationdate')
        self.form_fields = self.form_fields.omit('moreexcercise_registrationdate')

class CreditsViewlet(ViewletBase):
    """ Adds a help panel for the annotator. """
    index = ViewPageTemplateFile('credits-viewlet.pt')

    @property
    def credits(self):
        member = self.context.restrictedTraverse(
            '@@plone_portal_state').member()
        return member.getProperty('credits', 0)

class CreditsView(BrowserView):
    template = ViewPageTemplateFile('credits.pt')

    def __call__(self):
        buy = self.request.get('buy', None)
        if buy is not None:
            try:
                buy = int(buy)
            except ValueError:
                self.request['error'] = _(u'Please enter an integer value')
                return self.template()

            if buy<=0:
                self.request['error'] = _(u'Please enter a positive integer value')
                return self.template()
                
            # XXX Payment gateway integration here, perhaps some utility we
            # can look up and delegate to.

            member = self.context.restrictedTraverse(
                '@@plone_portal_state').member()
            credits = member.getProperty('credits', 0)
            member.setMemberProperties({'credits': credits + buy})
            IStatusMessage(self.request).addStatusMessage(_(u'Credit loaded.'))
            self.request['success'] = True

        return self.template()

    @property
    def cost(self):
        settings = queryUtility(IRegistry).forInterface(IEmasSettings)
        return settings.creditcost
