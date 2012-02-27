from zope.component import queryAdapter

from Products.CMFCore.utils import getToolByName
from plone.uuid.interfaces import IUUID

from siyavula.what.browser.questionslistviewlet \
    import QuestionsListViewlet as BaseQuestionsListViewlet

from emas.theme import MessageFactory as _


class QuestionsListViewlet(BaseQuestionsListViewlet):
    """ Specialise the siyavula.what viewlet to check if the service is enabled.
    """

    def allowQuestions(self):
        """ Check against the members enabled services.
        """
        view = self.context.restrictedTraverse('@@enabled-services')
        adapter = queryAdapter(self.context, name='siyavula.what.allowquestions')
        # if we cannot adapt it, it won't have the allowQuestions field.
        if not adapter:
            return False
        allowQuestions = getattr(self.context, 'allowQuestions', False)
        return allowQuestions and view.ask_expert_enabled

    def questions(self):
        """ Return all questions that have the current context set
            as 'relatedContent'.
        """
        view = self.context.restrictedTraverse('@@enabled-services')
        context = self.context
        uuid = IUUID(context)
        pc = getToolByName(context, 'portal_catalog')
        query = {'portal_type': 'siyavula.what.question',
                 'relatedContentUID': uuid,
                 'sort_on': 'created',
                }
        if not view.answer_database_enabled:
            pmt = getToolByName(self.context, 'portal_membership')
            member = pmt.getAuthenticatedMember()
            query['Creator'] = member.getId()
        brains = pc(query)
        return brains and [b.getObject() for b in brains] or []
