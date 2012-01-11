from Products.Five.browser import BrowserView
from plone.app.folder.folder import IATUnifiedFolder

from emas.theme import MessageFactory as _


class TableOfContentsHelpers(BrowserView):
    """ Helper methods and a template that renders only the table of contents.
    """
    def getContentItems(self, container=None):
        container = container or self.context
        return container.getFolderContents(full_objects=True)

    def isFolder(self, item):
        return IATUnifiedFolder.providedBy(item) and True or False
    
    def getTitle(self, item):
        """ If it does not have its own title, we fall back to id.
        """
        return item.Title() or item.getId()
