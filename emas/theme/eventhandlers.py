import logging
from DateTime import DateTime
from types import ListType
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

from emas.theme.userdataschema import IEmasUserDataSchema

LOGGER = logging.getLogger('emas.theme:eventhandlers:')

def add_subscribers(subscribers):
    update_subscription(subscribers, True)

def remove_subscribers(subscribers):
    update_subscription(subscribers, False)

def update_subscription(subscribers, new_state):
    for subscriber in subscribers:
        subscriber.setMemberProperties({'subscribe_to_newsletter': new_state})

def onUserInitialLogin(obj, event):
    try:
        set_welcome_message(obj, event)
        update_newsletter_subscription(obj, event)
        store_registration_date(obj, event)    
    except AttributeError:
	return

def onMemberPropsUpdated(obj, event):
    update_newsletter_subscription(obj, event)

def set_welcome_message(obj, event):
    plone_utils = getToolByName(obj, 'plone_utils')
    message = obj.restrictedTraverse('@@firstlogin')()
    plone_utils.addPortalMessage(message, 'info')

def update_newsletter_subscription(obj, event):

    memberid = obj.getId()

    portal_groups = getToolByName(obj, 'portal_groups')
    group_id = "newsletter_subscribers"

    if obj.getProperty('subscribe_to_newsletter', False):
        portal_groups.addPrincipalToGroup(memberid, group_id)
    else:
        portal_groups.removePrincipalFromGroup(memberid, group_id)

def store_registration_date(obj, event):
    memberid = obj.getId()
    pm = getSite().portal_membership
    member = pm.getMemberById(memberid)
    member.setMemberProperties(mapping={"registrationdate": DateTime()})
