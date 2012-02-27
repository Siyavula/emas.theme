from datetime import datetime

from plone.app.layout.viewlets.common import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from emas.theme import MessageFactory as _
from emas.theme.browser.views import NULLDATE
from emas.theme.browser.views import RegisterForMoreExerciseView 
from emas.theme.browser.views import RegisterToAccessAnswerDatabaseView
from emas.theme.browser.views import RegisterToAskQuestionsView

class RegisterToAskQuestionsViewlet(
    ViewletBase, RegisterToAskQuestionsView):

    """ Help users register to ask questions. """
    index = ViewPageTemplateFile(
        'templates/registertoaskquestions_viewlet.pt')

    def update(self):
        super(RegisterToAskQuestionsViewlet, self).update()
        if self.request.form.get('form.button.submit', '').lower() == 'register':
            self.handleRegister()
        return self.index()


class RegisterToAccessAnswerDatabaseViewlet(
    ViewletBase, RegisterToAccessAnswerDatabaseView):

    """ Help users register to access the answers database. """
    index = ViewPageTemplateFile(
        'templates/registertoaccessanswerdatabase_viewlet.pt')

    def update(self):
        super(RegisterToAccessAnswerDatabaseViewlet, self).update()
        if self.request.form.get('form.button.submit', '').lower() == 'register':
            self.handleRegister()
        return self.index()

class RegisterForMoreExerciseViewlet(
    ViewletBase, RegisterForMoreExerciseView):

    """ Help users register to access more exercise content. """
    index = ViewPageTemplateFile(
        'templates/registerformoreexercise_viewlet.pt')

    def update(self):
        super(RegisterForMoreExerciseViewlet, self).update()
        if self.request.form.get('form.button.submit', '').lower() == 'register':
            self.handleRegister()
        return self.index()
