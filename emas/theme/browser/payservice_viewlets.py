from datetime import datetime

from plone.app.layout.viewlets.common import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from emas.theme import MessageFactory as _
from emas.theme.browser.views import NULLDATE

ALLOWED_TYPES = ['Folder',
                 'rhaptos.xmlfile.xmlfile',
                 'rhaptos.compilation.section',
                 'rhaptos.compilation.compilation',
                ]

class BasePayServicesViewlet(ViewletBase):
    """ Common ancestor for pay services viewlets. """
    # these fields must be supplied by the inheriting classes.
    formsubmit_token = None
    formfield = None
    memberproperty = None

    @property
    def can_show(self):
        return self.context.portal_type in ALLOWED_TYPES

    @property
    def has_credits(self):
        pmt = getToolByName(self.context, 'portal_membership')
        member = pmt.getAuthenticatedMember()
        return member.getProperty('credits', 0) and True or False
    
    @property
    def is_registered(self):
        pmt = getToolByName(self.context, 'portal_membership')
        member = pmt.getAuthenticatedMember()
        regdate = member.getProperty(self.memberproperty)
        try:
            return regdate > NULLDATE
        except:
            return False

    def update(self):
        super(BasePayServicesViewlet, self).update()
        if self.request.form.get(self.formsubmit_token):
            enable_service = self.request.form.get(self.formfield)
            pmt = getToolByName(self.context, 'portal_membership')
            member = pmt.getAuthenticatedMember()
            regdate = NULLDATE
            if enable_service:
                regdate = datetime.date(datetime.now())
            member.setMemberProperties({self.memberproperty: regdate})


class RegisterToAskQuestionsViewlet(BasePayServicesViewlet):
    """ Help users register to ask questions. """
    index = ViewPageTemplateFile(
        'templates/registertoaskquestions_viewlet.pt')

    formsubmit_token = 'emas.theme.registertoaskquestions.submitted'
    formfield = 'registertoaskquestions'
    memberproperty = 'askanexpert_registrationdate'


class RegisterToAccessAnswerDatabaseViewlet(BasePayServicesViewlet):
    """ Help users register to access the answers database. """
    index = ViewPageTemplateFile(
        'templates/registertoaccessanswerdatabase_viewlet.pt')

    formsubmit_token = 'emas.theme.registertoaccessanswerdatabase.submitted'
    formfield = 'registertoaccessanswerdatabase'
    memberproperty = 'answerdatabase_registrationdate'


class RegisterForMoreExerciseViewlet(BasePayServicesViewlet):
    """ Help users register to access more exercise content. """
    index = ViewPageTemplateFile(
        'templates/registerformoreexercise_viewlet.pt')

    formsubmit_token = 'emas.theme.registerformoreexercise.submitted'
    formfield = 'registerformoreexercise'
    memberproperty = 'moreexercise_registrationdate'
