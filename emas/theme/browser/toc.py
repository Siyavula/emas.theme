from Acquisition import aq_inner

from zope.interface import implements
from zope.component import getMultiAdapter

from plone.app.folder.folder import IATUnifiedFolder
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder

from emas.theme import MessageFactory as _
from emas.theme.browser.interfaces import ITOC, ITOCView

class TOCQueryBuilder(NavtreeQueryBuilder):
    """Build a folder tree query suitable for table of contents
    """

    def __init__(self, context):
        NavtreeQueryBuilder.__init__(self, context)
        self.query['path'] = {'query': context.getPhysicalPath()}


class CatalogTOC(BrowserView):
    implements(ITOC)

    def toc(self):
        context = aq_inner(self.context)

        queryBuilder = TOCQueryBuilder(context)
        query = queryBuilder()

        strategy = getMultiAdapter((context, self), INavtreeStrategy)
        strategy.rootPath = '/'.join(context.getPhysicalPath())

        return buildFolderTree(context, obj=context, query=query, 
                               strategy=strategy)


class TOCView(BrowserView):
    implements(ITOCView)

    def createTOC(self):
        context = aq_inner(self.context)
        view = getMultiAdapter((context, self.request),
                               name='toc_builder_view')
        data = view.toc()
        properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(properties, 'navtree_properties')
        bottomLevel = navtree_properties.getProperty('bottomLevel', 0)
        # XXX: The recursion should probably be done in python code
        return context.portlet_navtree_macro(children=data.get('children', []),
                                             level=1, bottomLevel=bottomLevel)

