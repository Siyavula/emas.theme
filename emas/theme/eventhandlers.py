import datetime
from zope.component import createObject
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.content.folder import ATFolder

from emas.theme.browser.utils import getMemberServices
from emas.theme.browser.utils import getServiceUUIDs
from emas.theme.browser.views import is_expert

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
    today = datetime.date.today()
    trialend = today + datetime.timedelta(days=30)
    intelligent_practice_access = (
        'maths-grade-10',
        'maths-grade-11',
        'maths-grade-12',
        'science-grade-10',
        'science-grade-11',
        'science-grade-12',
    )

    # Make sure the user's service registration dates are correct
    properties = {'askanexpert_registrationdate': today,
                  'answerdatabase_registrationdate': today,
                  'moreexercise_registrationdate': today,
                  'answerdatabase_expirydate': trialend,
                  'moreexercise_expirydate': trialend,
                  'credits': 2,
                  'intelligent_practice_access': intelligent_practice_access,
                  'trialuser': True, 
                 }
    propsheet = obj.getPropertysheet('mutable_properties')
    for key, value in properties.items():
        propsheet.setProperty(obj, key, value)

def questionAsked(obj, event):
    """ Deduct a credit when a question is asked
    """
    if is_expert(obj):
        return

    context = obj.relatedContent.to_object

    service_uids = getServiceUUIDs(context)
    # there are no services so the user cannot pay for any.
    if service_uids is None or len(service_uids) < 1:
        return

    memberservices = getMemberServices(context, service_uids)
    if len(memberservices) < 1:
        raise RuntimeError("The user has no credits.")
    else:
        credits = memberservices[0].credits - 1
        memberservices[0].credits = credits

def questionDeleted(obj, event):
    """ Add a credit when a question is deleted.
    """
    if is_expert(obj):
        return
    pmt = getToolByName(obj, 'portal_membership')
    member = pmt.getMemberById(obj.Creator())
    credits = member.getProperty('credits') + 1
    member.setMemberProperties({'credits': credits})
