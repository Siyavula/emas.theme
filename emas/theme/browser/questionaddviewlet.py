from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from emas.theme import MessageFactory as _

class QuestionAddViewlet(ViewletBase):
    """ Display a form to add a new question.
    """
    index = ViewPageTemplateFile('questionaddviewlet_templates/addform.pt')

    def update(self):
        super(QuestionAddViewlet, self).update()
        if self.request.get('method', '').lower() == 'post':
            view = self.context.restrictedTraverse('@@add-question')
            question = view()
            self.request.response.redirect(self.context.absolute_url())
