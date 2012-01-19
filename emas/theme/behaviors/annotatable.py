from zope.interface import alsoProvides
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from z3c.form.interfaces import IEditForm, IAddForm

from zope.schema import Bool

from emas.theme import MessageFactory as _


class IAnnotatableContent(form.Schema):
    """ Marker/Form interface for Annotatable content behavior
    """

    form.fieldset(
        'settings',
        label=_(u'Settings'),
        fields=['enableAnnotations',],
        )

    enableAnnotations = Bool(
        title=_(u'label_enable_annotations', default=u'Enable Annotations'),
        required=False,
    )

    form.omitted('enableAnnotations')
    form.no_omit(IEditForm, 'enableAnnotations')
    form.no_omit(IAddForm, 'enableAnnotations')

alsoProvides(IAnnotatableContent,IFormFieldProvider)
