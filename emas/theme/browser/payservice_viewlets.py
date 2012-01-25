from DateTime import DateTime

from plone.app.layout.viewlets.common import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from emas.theme import MessageFactory as _


class BasePayServicesViewlet(ViewletBase):
    """ Common ancestor for pay services viewlets. """

    @property
    def has_credits(self):
        pmt = getToolByName(self.context, 'portal_membership')
        member = pmt.getAuthenticatedMember()
        return member.getProperty('credits', 0) and True or False

class RegisterToAskQuestionsViewlet(BasePayServicesViewlet):
    """ Help users register to ask questions. """

    index = ViewPageTemplateFile('templates/registertoaskquestions_viewlet.pt')
    NULLDATE = DateTime('1970/01/01 00:00:00')

    def update(self):
        super(RegisterToAskQuestionsViewlet, self).update()
        if self.request.form.get('emas.theme.registertoaskquestions.submitted'):
            enable_service = self.request.form.get('registertoaskquestions')
            pmt = getToolByName(self.context, 'portal_membership')
            member = pmt.getAuthenticatedMember()
            regdate = self.NULLDATE
            if enable_service:
                regdate = DateTime()
            member.setMemberProperties(
                {'askanexpert_registrationdate': regdate})
    
    @property
    def is_registered(self):
        pmt = getToolByName(self.context, 'portal_membership')
        member = pmt.getAuthenticatedMember()
        regdate = member.getProperty('askanexpert_registrationdate')
        return regdate > self.NULLDATE and True or False
        
