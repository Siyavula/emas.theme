from zope.component import createObject
from Products.CMFCore.permissions import ModifyPortalContent
from Products.ATContentTypes.content.folder import ATFolder

def onMemberJoined(obj, event):
    portal = obj.restrictedTraverse('@@plone_portal_state').portal()
    transactions = portal.transactions

    memberid = obj.getId()

    # Because all permissions have been disabled on transactions, we cannot use
    # invokeFactory
    folder = ATFolder(memberid)
    transactions._setObject(memberid, folder)
    transactions.reindexObject()

    # Finally, change its permissions
    folder.manage_permission(ModifyPortalContent, roles=[], acquire=0)