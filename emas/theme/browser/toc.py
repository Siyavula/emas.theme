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
        title = item.Title()
        # so it does not have its own title, now we see if it has a default
        # page and use that title.
        if title is None or len(title) < 1:
            title = 'Unknown'
            page_id = item.getDefaultPage()
            if page_id:
                page = item._getOb(page_id)
                title = page.Title()
        return title
