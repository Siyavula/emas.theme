from Products.CMFCore.utils import getToolByName

def getAuthedMemberCredits(context):
    pmt = getToolByName(context, 'portal_membership')
    member = pmt.getAuthenticatedMember()
    current_credits = member.getProperty('credits', 0)
    return current_credits
