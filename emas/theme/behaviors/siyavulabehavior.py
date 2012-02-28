from zope.interface import alsoProvides
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider

from emas.theme.behaviors.annotatable import IAnnotatableContent
from siyavula.what.behaviors.allowquestionsbehavior import \
    IAllowQuestionsBehavior
from plone.app.dexterity.behaviors.nextprevious import INextPreviousToggle

class ISiyavulaBehavior(form.Schema):
    """ Behaviour to aggregate all the behaviours we want on the
        "settings" tab.
    """

    form.fieldset('settings', label=u"Settings",
                  fields=['nextPreviousEnabled', 'enableAnnotations',
                          'allowQuestions'])

alsoProvides(ISiyavulaBehavior, IFormFieldProvider)
