from Products.Archetypes.utils import shasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from siyavula.what.browser.questionaddviewlet \
    import QuestionAddViewlet as BaseQuestionAddViewlet

from emas.theme.browser.views import is_expert
from emas.theme import MessageFactory as _


class QuestionAddViewlet(BaseQuestionAddViewlet):
    """ A little safer way to see if questions are allowed on
        the given context.
    """

    index = ViewPageTemplateFile('templates/addquestion.pt')

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
            return super(QuestionAddViewlet, self).render()
        else:
            return ""
    
