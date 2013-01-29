import logging

from types import ListType
from Products.CMFCore.utils import getToolByName

from emas.theme.userdataschema import IEmasUserDataSchema

LOGGER = logging.getLogger('emas.theme:eventhandlers:')

def onNewsLetterEdited(obj, event):
    pmt = getToolByName(obj, 'portal_membership')
    memberids = set(pmt.listMemberIds())
    subscribers = set(obj.ploneReceiverMembers)
    nonsubscribers = memberids.difference(subscribers)

    subscribers = [pmt.getMemberById(s) for s in subscribers]
    add_subscribers(subscribers)

    nonsubscribers = [pmt.getMemberById(s) for s in nonsubscribers]
    remove_subscribers(nonsubscribers)

def add_subscribers(subscribers):
    update_subscription(subscribers, True)

def remove_subscribers(subscribers):
    update_subscription(subscribers, False)

def update_subscription(subscribers, new_state):
    for subscriber in subscribers:
        subscriber.setMemberProperties({'subscribe_to_newsletter': new_state})

def onUserInitialLogin(obj, event):
    set_welcome_message(obj, event)
    update_newsletter_subscription(obj, event)

def onMemberPropsUpdated(obj, event):
    update_newsletter_subscription(obj, event)

def set_welcome_message(obj, event):
    plone_utils = getToolByName(obj, 'plone_utils')
    message = obj.restrictedTraverse('@@firstlogin')()
    plone_utils.addPortalMessage(message, 'info')

def update_newsletter_subscription(obj, event):
    portal = obj.restrictedTraverse('@@plone_portal_state').portal()
    newsletters = portal._getOb('newsletters')
    newsletter = newsletters._getOb('everything-news')
    receivers = ListType(newsletter.ploneReceiverMembers)
    memberid = obj.getId()

    if obj.getProperty('subscribe_to_newsletter', False):
        # subscribe member by adding the memberid to receivers list
        if memberid in receivers:
            LOGGER.debug('Member:%s is already in newsletter.' % memberid)
        else:
            receivers.append(memberid)
    else:
        # unsubscribe member by removing the memberid from receivers list
        if memberid not in receivers:
            LOGGER.debug('Member:%s is not in newsletter.' % memberid)
        else:
            receivers.remove(memberid)
    newsletter.ploneReceiverMembers = receivers
