from zope.component import queryAdapter

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
        adapter = queryAdapter(self.context, name='siyavula.what.allowquestions')
        # if we cannot adapt it, it won't have the allowQuestions field.
        if not adapter:
            return False
        allowQuestions = getattr(self.context, 'allowQuestions', False)
        return allowQuestions and view.ask_expert_enabled
