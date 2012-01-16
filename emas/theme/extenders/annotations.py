from zope.interface import implements

from Products.Archetypes.Widget import BooleanWidget
from Products.Archetypes.public import BooleanField

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender

from emas.theme.interfaces import IEmasThemeLayer
from emas.theme import MessageFactory as _

class _AnnotationsExtensionField(ExtensionField, BooleanField): pass

class AnnotationsExtender(object):
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    layer = IEmasThemeLayer

    fields = [
        _AnnotationsExtensionField(
            "enableAnnotations",
            default = False,
            widget = BooleanWidget(
                label=_(u"Enable Annotations"),
                description=_(u"Enable the annotator for this content."),
            ),
            schemata='settings',
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
