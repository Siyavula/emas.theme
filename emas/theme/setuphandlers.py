import logging
from StringIO import StringIO

from zope.interface import directlyProvides, directlyProvidedBy

from Products.ATContentTypes.permission import ModifyConstrainTypes
from Products.ATContentTypes.permission import ModifyViewTemplate
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

    # add folder for community site
    if not portal.hasObject('community'):
        portal.invokeFactory(id='community', type_name='Folder',
                             title='Siyavula Community')

        community = portal.community
        directlyProvides(community, directlyProvidedBy(community),
                         INavigationRoot)

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
    
    # all extra items we require
    items = [
        {'id': 'newsletters',
        'type': 'Folder',
        'title': 'Everything News',
        'allowed_types': ['EasyNewsletter',],
        'exclude_from_nav':True,
        'workflowid': 'simple_publication_workflow',
        'publish': True,
        'sub_items': [{'id': 'everything-news',
                        'type': 'EasyNewsletter',
                        'title': 'Everything Newsletter',
                        'exclude_from_nav':True,
                      },
                     ]
        },
    ]

    for prop_dict in items:
        if not portal.hasObject(prop_dict['id']):
            portal.invokeFactory(type_name=prop_dict['type'],
                id=prop_dict['id'],
                title=prop_dict['title'],
                exclude_from_nav=prop_dict.get('exclude_from_nav', False),
            ) 

        folder = portal._getOb(prop_dict['id'])

        # Nobody is allowed to modify the constraints or tweak the
        # display here
        folder.manage_permission(ModifyConstrainTypes, roles=[])
        folder.manage_permission(ModifyViewTemplate, roles=[])
        
        if prop_dict.get('publish', False):
            wf = getToolByName(portal, 'portal_workflow')
            wfid = prop_dict['workflowid']
            status = wf.getStatusOf(wfid, folder)
            if status and status['review_state'] != 'published':
                wf.doActionFor(folder, 'publish')
                folder.reindexObject()
       
        # create required sub-items
        for subitem_props in prop_dict['sub_items']:
            if not folder.hasObject(subitem_props['id']):
                folder.invokeFactory(type_name=subitem_props['type'],
                    id=subitem_props['id'],
                    title=subitem_props['title'],
                    exclude_from_nav=subitem_props.get('exclude_from_nav', False),
                ) 
    

def install(context):
    if context.readDataFile('emas.theme-marker.txt') is None:
        return
    site = context.getSite()

    reorder_contenttype_registry(site)
    setupPortalContent(site)
