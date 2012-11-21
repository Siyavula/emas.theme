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
        newsletter = newsletters._getOb('everything-news')
        receivers = newsletter.ploneReceiverMembers
        memberid = obj.getId()
        if memberid in receivers:
            LOGGER.debug('Member:%s is already in newsletter.' % memberid)
        else:
            receivers.append(memberid)
            newsletter.ploneReceiverMembers = receivers

def onMemberPropsUpdated(obj, event):
    subscribe_to_newsletters(obj, event)
