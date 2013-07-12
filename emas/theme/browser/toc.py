import urlparse
from Acquisition import aq_base, aq_inner

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

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

        if self.has_practise_content(self.context):
            # get the chapter context from the last link of the chapter
            lastitem_url = result[len(result)-1].absolute_url()
            lastitem_type = result[len(result)-1].portal_type
            # only add 'practice this chapter now' if the other items in the 
            # list are book links
            if lastitem_type == 'rhaptos.xmlfile.xmlfile':
                chapter = lastitem_url.split('/')[-2]
                chapter = '/' + chapter    
                result.append(self._practice_url(chapter))

        return result

    def isFolder(self, item):
        return bool(getattr(aq_base(aq_inner(item)), 'isPrincipiaFolderish',
                            False))
    
    def getTitle(self, item):
        """ If it does not have its own title, we fall back to id.
        """
        return item.Title() or item.getId()

    def has_practise_content(self, context):
        retVal = True
        paths_without_practise_content = [
            '/emas/maths/grade-10-mathematical-literacy',
            '/emas/maths/grade-11-mathematical-literacy',
            '/emas/maths/grade-12-mathematical-literacy',
        ]
        path = self.context.getPhysicalPath()
        if path:
            path = '/'.join(path[:4])
            if path in paths_without_practise_content:
                retVal = False

        return retVal

    def _practice_url(self, chapter):
        absolute_url = self.context.absolute_url()
        title = 'Practise this chapter now'
        parts = urlparse.urlparse(self.context.absolute_url())
        newparts = urlparse.ParseResult(parts.scheme,
                                        parts.netloc,
                                        '/@@practice' + parts.path + chapter,
                                        parts.params,
                                        parts.query,
                                        parts.fragment)
        url = urlparse.urlunparse(newparts)
        tmp_dict = {
            'Title': title,
            'absolute_url': url,
            'css_class': 'practice-link',
        }
        return tmp_dict

