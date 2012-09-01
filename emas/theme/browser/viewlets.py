from zope.interface import implements
from zope.component import getMultiAdapter

from Acquisition import aq_inner
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.uuid.interfaces import IUUID
from plone.app.layout.viewlets import common
from siyavula.what.browser.viewlets import QAViewlet as BaseQAViewlet
from webcouturier.dropdownmenu.browser.interfaces import IDropdownMenuViewlet

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
        if self.allowQuestions():
            return super(QAViewlet, self).render()
        else:
            return ""


class DropdownMenuViewlet(common.GlobalSectionsViewlet):
    """A custom version of the global navigation class that has to have
       dropdown menus for global navigation tabs objects
    """
    implements(IDropdownMenuViewlet)

    index = ViewPageTemplateFile('templates/dropdown.pt')

    def update(self):
        context = aq_inner(self.context)
        portal_state_view = getMultiAdapter((context, self.request),
                                             name='plone_portal_state')
        navroot = portal_state_view.navigation_root()
        self.site_url = navroot.absolute_url()

