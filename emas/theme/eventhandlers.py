import logging

from Products.CMFCore.utils import getToolByName


LOGGER = logging.getLogger('emas.theme:eventhandlers:')

def onUserInitialLogin(obj, event):
    set_welcome_message(obj, event)
    subscribe_to_newsletters(obj, event)

def set_welcome_message(obj, event):
    plone_utils = getToolByName(obj, 'plone_utils')
    message = obj.restrictedTraverse('@@firstlogin')()
    plone_utils.addPortalMessage(message, 'info')

def subscribe_to_newsletters(obj, event):
    subscribe_prefix = 'subscribe_to_'

    portal = obj.restrictedTraverse('@@plone_portal_state').portal()
    newsletters = portal._getOb('newsletters')

    # get a list of available newsletters
    newsletter_names = newsletters.objectIds()
    # if we don't have newsletters configured, warn and carry on.
    if not newsletter_names:
        LOGGER.warn('No newsletters configured')
        return

    if obj.getProperty('subscribe_to_newsletter', False):
        portal.REQUEST['subscriber'] = obj.getProperty('email')
        portal.REQUEST['fullname'] = obj.getProperty('fullname')
        portal.REQUEST['salutation'] = obj.getProperty('salutation', '')
        portal.REQUEST['organisation'] = obj.getProperty('school')
        nl_path = '/'.join(newsletters._getOb(name).getPhysicalPath())
        portal.REQUEST['newsletter'] = nl_path

        view = portal.restrictedTraverse('@@register-subscriber')
        view()

def onMemberPropsUpdated(obj, event):
    subscribe_to_newsletters(obj, event)
