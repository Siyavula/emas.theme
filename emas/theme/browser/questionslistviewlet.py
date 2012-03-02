from Products.Archetypes.utils import shasattr

from Products.CMFCore.utils import getToolByName
from plone.uuid.interfaces import IUUID

from siyavula.what.browser.questionslistviewlet \
    import QuestionsListViewlet as BaseQuestionsListViewlet
from emas.theme.browser.views import is_expert

from emas.theme import MessageFactory as _


class QuestionsListViewlet(BaseQuestionsListViewlet):
    """ Specialise the siyavula.what viewlet to check if the service is enabled.
    """

    def allowQuestions(self):
        """ Check against the members enabled services.
        """
        context = self.context
        view = context.restrictedTraverse('@@enabled-services')
        allowQuestions = False
        if shasattr(context, 'allowQuestions'):
            allowQuestions = getattr(context, 'allowQuestions')
        return allowQuestions and view.ask_expert_enabled

    def questions(self):
        """ Return all questions that have the current context set
            as 'relatedContent'.
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
