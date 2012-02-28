from Products.Archetypes.utils import shasattr

from siyavula.what.browser.questionaddviewlet \
    import QuestionAddViewlet as BaseQuestionAddViewlet

from emas.theme import MessageFactory as _


class QuestionAddViewlet(BaseQuestionAddViewlet):
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
