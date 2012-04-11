import datetime
from zope.component import createObject
from Products.CMFCore.permissions import ModifyPortalContent
from Products.ATContentTypes.content.folder import ATFolder

from emas.theme.browser.views import is_expert
from emas.theme.browser.views import NULLDATE

def onMemberJoined(obj, event):
    portal = obj.restrictedTraverse('@@plone_portal_state').portal()
    transactions = portal.transactions

    memberid = obj.getId()

    # Because all permissions have been disabled on transactions, we cannot use
    # invokeFactory
    if not memberid in transactions.objectIds():
        folder = ATFolder(memberid)
        transactions._setObject(memberid, folder)
        transactions.reindexObject()

        # Finally, change its permissions
        folder.manage_permission(ModifyPortalContent, roles=[], acquire=0)
    

    # 30 days free trial with 2 questions
    trialend = datetime.date.today() + datetime.timedelta(days=30)

    # Make sure the user's service registration dates are correct
    properties = {'askanexpert_registrationdate': trialend,
                  'answerdatabase_registrationdate': trialend,
                  'moreexercise_registrationdate': trialend,
                  'credits': 2,
                 }
    propsheet = obj.getPropertysheet('mutable_properties')
    for key, value in properties.items():
        propsheet.setProperty(obj, key, value)

def questionAsked(obj, event):
    """ Deduct a credit when a question is asked
    """
    if is_expert(obj):
        return

    member = obj.restrictedTraverse('@@plone_portal_state').member()
    credits = member.getProperty('credits') - 1
    if credits < 0:
        raise RuntimeError("Credits can't be less than zero")
    member.setMemberProperties({'credits': credits})
