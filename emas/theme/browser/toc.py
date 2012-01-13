from Acquisition import aq_base, aq_inner

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from plone.app.folder.folder import IATUnifiedFolder

from emas.theme import MessageFactory as _

class TableOfContents(BrowserView):
    """ Helper methods and a template that renders only the table of contents.
    """
    def getContentItems(self, container=None):

        portal_properties = getToolByName(self.context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        portal_catalog = getToolByName(self.context, 'portal_catalog')

        blacklist = navtree_properties.getProperty('metaTypesNotToList', ())
        all_types = portal_catalog.uniqueValuesFor('portal_type')

        contentFilter = dict(
            portal_type=[t for t in all_types if t not in blacklist]
            )
        container = container or self.context

        idsNotToList = navtree_properties.getProperty('idsNotToList', ())
        result = []
        for brain in container.getFolderContents(contentFilter):
            if not (brain.getId in idsNotToList or brain.exclude_from_nav):
                result.append(brain.getObject())
        return result

    def isFolder(self, item):
        return bool(getattr(aq_base(aq_inner(item)), 'isPrincipiaFolderish',
                            False))
    
    def getTitle(self, item):
        """ If it does not have its own title, we fall back to id.
        """
        return item.Title() or item.getId()
