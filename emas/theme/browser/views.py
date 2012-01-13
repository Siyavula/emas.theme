from zope.component import queryUtility

from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from upfront.shorturl.browser.views import RedirectView

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

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
