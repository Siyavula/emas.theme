from Products.Archetypes.utils import shasattr

from Products.CMFCore.utils import getToolByName
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from siyavula.what.browser.viewlets import QAViewlet as BaseQAViewlet
from emas.theme.browser.views import is_expert
from emas.theme import MessageFactory as _


class QAViewlet(BaseQAViewlet):
    """ Specialise the siyavula.what viewlet to check if the service is enabled.
    """

    def questions(self):
        """ Return all questions that have the current context set
            as 'relatedContent'.

            If the user is not registered for the service, we still
            return all the questions (and answers) that he owns.
            That way, eventhough the service subscription has expired,
            the user still has access to the questions and answers
            for which he paid.
        """
        context = self.context
        uuid = IUUID(context)
        pc = getToolByName(context, 'portal_catalog')
        query = {'portal_type': 'siyavula.what.question',
                 'relatedContentUID': uuid,
                 'sort_on': 'created',
                }
        if is_expert(self.context):
            brains = pc(query)
            return brains and [b.getObject() for b in brains] or []

        view = self.context.restrictedTraverse('@@enabled-services')
        if not view.answer_database_enabled:
            pmt = getToolByName(self.context, 'portal_membership')
            member = pmt.getAuthenticatedMember()
            query['Creator'] = member.getId()
        brains = pc(query)
        return brains and [b.getObject() for b in brains] or []

    def allowQuestions(self):
        """ Check against the members enabled services.
        """
        context = self.context
        allowQuestions = False
        if shasattr(context, 'allowQuestions'):
            allowQuestions = getattr(context, 'allowQuestions')
        return allowQuestions

    def is_enabled(self):
        """
        """
        context = self.context
        view = context.restrictedTraverse('@@enabled-services')
        return view.ask_expert_enabled

    def render(self):
        """ We render an empty string when a specific piece of content
            does not allow questions.
        """
        if self.allowQuestions() and self.is_enabled():
            return super(QAViewlet, self).render()
        else:
            return ""
