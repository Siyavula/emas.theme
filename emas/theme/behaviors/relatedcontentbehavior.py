from zope.interface import alsoProvides
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider

from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from emas.theme import MessageFactory as _


class IRelatedContent(form.Schema):
    """
       Marker/Form interface for Related content behavior
    """
    relatedContent = RelationChoice(
        title=_(u'label_content_item', default=u'Related Content'),
        source=ObjPathSourceBinder(),
        required=False,
    )

alsoProvides(IRelatedContent,IFormFieldProvider)
