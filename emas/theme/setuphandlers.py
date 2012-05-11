import logging
from StringIO import StringIO

from zope.interface import directlyProvides, directlyProvidedBy

from plone.app.layout.navigation.interfaces import INavigationRoot

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ModifyPortalContent, AddPortalContent
from Products.CMFCore.permissions import DeleteObjects

log = logging.getLogger('emas.theme-setuphandlers')

def reorder_contenttype_registry(portal):
    registry = getToolByName(portal, 'content_type_registry')
    # move cnxml and cnxml+ predicate to the top
    registry.reorderPredicate('cnxml', 0)
    registry.reorderPredicate('cnxmlplus', 1)

def setupPortalContent(portal):
    # delete all content in the root
    for objId in ('front-page', 'Members', 'news', 'events'):
        if portal.hasObject(objId):
            portal.manage_delObjects(ids=objId)

    # add folder for maths
    if not portal.hasObject('maths'):
        portal.invokeFactory(id='maths', type_name='Folder',
                             title='Everything Maths')

        maths = portal.maths
        directlyProvides(maths, directlyProvidedBy(maths), INavigationRoot)
        for i in range(10,13):
            objId = 'grade-%s' % i
            objTitle = 'Grade %s Mathematics' % i
            maths.invokeFactory(id=objId, type_name='Folder',
                                title=objTitle)
            obj = maths[objId]
            obj.setNextPreviousEnabled(True)


    # add folder for science
    if not portal.hasObject('science'):
        portal.invokeFactory(id='science', type_name='Folder',
                             title='Everything Science')
        science = portal.science
        directlyProvides(science, directlyProvidedBy(science), INavigationRoot)
        for i in range(10,13):
            objId = 'grade-%s' % i
            objTitle = 'Grade %s Physics' % i
            science.invokeFactory(id=objId, type_name='Folder',
                                title=objTitle)
            obj = science[objId]
            obj.setNextPreviousEnabled(True)

    # disable tabs
    pprop = getToolByName(portal, 'portal_properties')
    pprop.site_properties._updateProperty('disable_folder_sections', True)

    # add index.cnxml as default page
    pprop = getToolByName(portal, 'portal_properties')
    default_pages = list(pprop.site_properties.getProperty('default_page'))
    if 'index.cnxml' not in default_pages:
        default_pages.append('index.cnxml')
    if 'index.cnxmlplus' not in default_pages:
        default_pages.append('index.cnxmlplus')
    pprop.site_properties._updateProperty('default_page', default_pages)

    # Add a folder for transactions
    if not portal.hasObject('transactions'):
        portal.invokeFactory(id='transactions', type_name='Folder',
                             title='Transactions')
        transactions = portal.transactions

        # Turn off permissions so nobody can add, modify or delete
        transactions.manage_permission(ModifyPortalContent, roles=[], acquire=0)
        transactions.manage_permission(AddPortalContent, roles=[], acquire=0)
        transactions.manage_permission(DeleteObjects, roles=[], acquire=0)


def install(context):
    if context.readDataFile('emas.theme-marker.txt') is None:
        return
    site = context.getSite()

    reorder_contenttype_registry(site)
    setupPortalContent(site)
