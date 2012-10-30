from Products.CMFCore.utils import getToolByName


def onUserInitialLogin(obj, event):
    plone_utils = getToolByName(obj, 'plone_utils')
    message = obj.restrictedTraverse('@@firstlogin')()
    plone_utils.addPortalMessage(message, 'info')
