from zope.interface import implements

from Products.Archetypes.Widget import BooleanWidget
from Products.Archetypes.public import BooleanField

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender

import logging
LOG = logging.getLogger('NavigationExtender')

class _NavigationRestrictionExtensionField(ExtensionField, BooleanField): pass

class NavigationRestrictionsExtender(object):
    implements(ISchemaExtender)

    fields = [
        _NavigationRestrictionExtensionField(
            "restrictNextPreviousNavigation",
            default = False,
            widget = BooleanWidget(
                label=u"Restrict navigation",
                description=u"Limit next/previous navigation to this folder and its children.",
            ),
            schemata='settings',
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

