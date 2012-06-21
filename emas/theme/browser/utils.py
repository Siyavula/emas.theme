from datetime import date
from Products.CMFCore.utils import getToolByName
from plone.uuid.interfaces import IUUID


def getSubjectAndGrade(context):
    """
        We trust in the structure of the content. Currently, this is
        /[subject]/[grade]/[content]

        Less than 4 elements means this was called on a context
        that does not have subject and grade as part of the path.
        We return the tuple ('none', 'none'), because there are no
        grades or subjects titled 'none'.
    """
    ppath = context.getPhysicalPath()
    if len(ppath) < 4:
        return ('none', 'none')
    return context.getPhysicalPath()[2:4]


def getServiceUUIDs(context):
    subject, grade = getSubjectAndGrade(context)
    pc = getToolByName(context, 'portal_catalog')
    query = {'portal_type': 'emas.app.service',
             'subject': subject,
             'grade': grade}
    service_uids = [IUUID(b.getObject()) for b in pc(query)]
    return service_uids


def getPracticeServiceUUIDS(context):
    subject, grade = getSubjectAndGrade(context)
    pc = getToolByName(context, 'portal_catalog')
    query = {'portal_type': 'emas.app.service',
             'subject': subject,
             'grade': grade,
             'Title': 'practice'}
    service_uids = [IUUID(b.getObject()) for b in pc(query)]
    return service_uids


def getMemberServices(context, service_uids):
    pmt = getToolByName(context, 'portal_membership')
    member = pmt.getAuthenticatedMember()
    query = {'portal_type': 'emas.app.memberservice',
             'memberid': member.getId(),
             'serviceuid': service_uids,
             'sort_on': 'expiry_date'
            }
    pc = getToolByName(context, 'portal_catalog')
    memberservices = [b.getObject() for b in pc(query)]
    return memberservices


def getMemberCredits(context):
    credits = 0

    service_uids = getServiceUUIDs(context)
    if service_uids is None or len(service_uids) < 1:
        return 0

    memberservices = getMemberServices(context, service_uids)
    if len(memberservices) < 1:
        return 0 

    for ms in memberservices:
        credits += ms.credits
    return credits


def getMemberServiceExpiryDate(context):
    expiry_date = None

    service_uids = getServiceUUIDs(context)
    if service_uids is None or len(service_uids) < 1:
        return None 
    
    memberservices = getMemberServices(context, service_uids)
    if len(memberservices) < 1:
        return  None

    for ms in memberservices:
        expiry_date = ms.expiry_date

    return expiry_date

def getPracticeServiceExpiryDate(context):
    service_uids = getPracticeServiceUUIDS(context)

    if service_uids is None or len(service_uids) < 1:
        return None
    
    memberservices = getMemberServices(context, service_uids)
    if len(memberservices) < 1:
        return  None
    
    return memberservices[0].expiry_date
