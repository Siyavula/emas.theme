from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from emas.theme import MessageFactory as _


class IRelatedContent(form.Schema):
    """
       Marker/Form interface for Related Content
    """
    relatedContent = RelationChoice(
        title=_(u'label_content_item', default=u'Related Content'),
        source=ObjPathSourceBinder(),
        required=False,
    )
alsoProvides(IRelatedContent,IFormFieldProvider)


def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)

class RelatedContent(object):
    """
       Adapter for Related Content
    """
    implements(IRelatedContent)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context
