import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import quickInstallProduct
from plone.app.testing import logout, login, setRoles

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
        import Products.EasyNewsletter
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
        self.loadZCML(package=Products.EasyNewsletter)
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

TEST_USER_ID = 'emastestuser'
TEST_USER_PWD = '12345'

class BaseFunctionalTestCase(unittest.TestCase):
    """
    """
    layer = INTEGRATION_TESTING

    def setUp(self):
        super(BaseFunctionalTestCase, self).setUp()
        self.portal = self.layer['portal']
        acl_users = getToolByName(self.portal, 'acl_users')
        acl_users.userFolderAddUser(TEST_USER_ID, TEST_USER_PWD, ['Member'], [])
        self.login(TEST_USER_ID)

    def login(self, userid=None):
        userid = userid or TEST_USER_ID
        login(self.portal, userid)

    def logout(self):
        logout()

    def setRoles(self, newroles, userid=None):
        userid = userid or TEST_USER_ID
        setRoles(self.portal, TEST_USER_ID, newroles)
