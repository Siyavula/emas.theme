from zope.component import queryUtility
from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from emas.theme.interfaces import IEmasSettings
from emas.theme import MessageFactory as _

class EmasSettingsForm(RegistryEditForm):
    schema = IEmasSettings
    label = _(u'EMAS Settings')
    description = _(u"Use the settings below to configure "
                    u"emas.theme for this site")

class EmasControlPanel(ControlPanelFormWrapper):
    form = EmasSettingsForm

class AnnotatorConfig(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(IEmasSettings)

    def accountId(self):
        return self.settings.accountid

    def annotatorStore(self):
        return self.settings.store

    def userId(self):
        import pdb; pdb.set_trace()
        member = self.context.restrictedTraverse(
            '@@plone_portal_state').member()
        return member.getId()
