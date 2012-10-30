from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import quickInstallProduct

from Products.PloneTestCase import PloneTestCase as ptc

from plone.testing import z2

PROJECTNAME = "emas.theme"

class TestCase(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.registry
        import plone.resource
        import plone.app.theming
        import plone.app.folder
        import rhaptos.xmlfile
        import collective.topictree
        import webcouturier.dropdownmenu
        import emas.transforms
        import rhaptos.cnxmltransforms
        import rhaptos.compilation
        import upfront.shorturl
        import fullmarks.mathjax
        import siyavula.what
        import emas.app
        import emas.theme
        self.loadZCML(package=plone.app.registry)
        self.loadZCML(package=plone.resource)
        self.loadZCML(package=plone.app.theming)
        self.loadZCML(package=rhaptos.xmlfile)
        self.loadZCML(package=collective.topictree)
        self.loadZCML(package=webcouturier.dropdownmenu)
        self.loadZCML(package=emas.transforms)
        self.loadZCML(package=rhaptos.cnxmltransforms)
        self.loadZCML(package=rhaptos.compilation)
        self.loadZCML(package=upfront.shorturl)
        self.loadZCML(package=fullmarks.mathjax)
        self.loadZCML(package=siyavula.what)
        self.loadZCML(package=emas.app)
        self.loadZCML(package=emas.theme)
        self.loadZCML('overrides.zcml', package=emas.theme)

    def setUpPloneSite(self, portal):
        quickInstallProduct(portal, 'emas.theme')
        self.applyProfile(portal, '%s:default' % PROJECTNAME)

    def tearDownZope(self, app):
        z2.uninstallProduct(app, PROJECTNAME)

FIXTURE = TestCase()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name="fixture:Integration")


class BaseFunctionalTestCase(ptc.FunctionalTestCase):
    """
    """
