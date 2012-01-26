from siyavula.what.browser.questionaddviewlet \
    import QuestionAddViewlet as BaseQuestionAddViewlet

from emas.theme import MessageFactory as _


class QuestionAddViewlet(BaseQuestionAddViewlet):
    """ Specialise the siyavula.what viewlet to check if the service is enabled.
    """

    def allowQuestions(self):
        """ Check against the members enabled services.
        """
        view = self.context.restrictedTraverse('@@enabled-services')
        return view.ask_expert_enabled
