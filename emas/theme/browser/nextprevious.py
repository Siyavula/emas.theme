from zope.interface import implements
from zope.component import adapts
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IContentish
from plone.app.layout.nextprevious.interfaces import INextPreviousProvider
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.folder.folder import IATUnifiedFolder


class NextPrevious(object):
    """ adapter for acting as a next/previous provider """
    implements(INextPreviousProvider)
    adapts(IATUnifiedFolder)

    def __init__(self, context):
        self.context = context
        props = getToolByName(context, 'portal_properties').site_properties
        self.vat = props.getProperty('typesUseViewActionInListings', ())
        self.security = getSecurityManager()
        order = context.getOrdering()
        if not isinstance(order, list):
            order = order.idsInOrder()
        if not isinstance(order, list):
            order = None
        self.order = order

    @property
    def enabled(self):
        includeInNav = not self.context.getExcludeFromNav() 
        nextPreviousEnabled = self.context.getNextPreviousEnabled()
        # only report 'enabled' True when both conditions are met
        return includeInNav and nextPreviousEnabled

    def getFirstItem(self):
        items = self.context.objectValues()[:]
        return items and items[0] or None

    def getLastItem(self):
        items = self.context.objectValues()[:]
        items.reverse()
        return items and items[0] or None

    def isFirstItem(self, obj):
        if obj is None:
            raise TypeError("Cannot compare 'None' to objects in container.")
        firstItem = self.getFirstItem()
        return obj == firstItem and True or False

    def isLastItem(self, obj):
        if obj is None:
            raise TypeError("Cannot compare 'None' to objects in container.")
        lastItem = self.getLastItem()
        return obj == lastItem and True or False

    def getNextItem(self, obj, camefrom=None):
        """ return info about the next item in the container """
        if not self.order:
            return None
        if self.isLastItem(obj):
            return None
        pos = self.context.getObjectPosition(obj.getId())
        for oid in self.order[pos+1:]:
            data = self.getData(self.context[oid])
            if data:
                return data
        # couldn't find one, let's see of our parent knows
        if not self.isLastItem(obj):
            parent = INextPreviousProvider(self.context.aq_parent)
            if parent and parent.enabled:
                return parent.getNextItem(self.context, camefrom)
        return None

    def getPreviousItem(self, obj, camefrom=None):
        """ return info about the previous item in the container """
        if not self.order:
            return None
        order_reversed = list(reversed(self.order))
        pos = order_reversed.index(obj.getId())
        for oid in order_reversed[pos+1:]:
            data = self.getData(self.context[oid])
            if data:
                return data
        # couldn't find one, let's see of our parent knows
        if self.isFirstItem(obj) and INavigationRoot.providedBy(self.context):
            return None
        else:
            parent = INextPreviousProvider(self.context.aq_parent)
            if parent and parent.enabled:
                return parent.getPreviousItem(self.context, camefrom)
        return None

    def getData(self, obj):
        """ return the expected mapping, see `INextPreviousProvider` """
        if not self.security.checkPermission('View', obj):
            return None
        elif not IContentish.providedBy(obj):
            # do not return a not contentish object
            # such as a local workflow policy for example (#11234)
            return None
        # pay attention to the 'excludedFromNav' attribute itself too
        elif obj.getExcludeFromNav():
            return None

        ptype = obj.portal_type
        url = obj.absolute_url()
        if ptype in self.vat:       # "use view action in listings"
            url += '/view'
        return dict(id=obj.getId(), url=url, title=obj.Title(),
            description=obj.Description(), portal_type=ptype)
