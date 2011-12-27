from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from plone.testing import z2

PROJECTNAME = "emas.theme"

class TestCase(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import rhaptos.xmlfile
        import rhaptos.cnxmltransforms
        import rhaptos.compilation
        import emas.theme
        self.loadZCML(package=rhaptos.xmlfile)
        self.loadZCML(package=rhaptos.cnxmltransforms)
        self.loadZCML(package=rhaptos.compilation)
        self.loadZCML(package=emas.theme)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, '%s:default' % PROJECTNAME)

    def tearDownZope(self, app):
        z2.uninstallProduct(app, PROJECTNAME)

FIXTURE = TestCase()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name="fixture:Integration")
