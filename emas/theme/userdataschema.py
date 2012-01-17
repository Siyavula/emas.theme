from zope.interface import implements
from zope.schema import Int
from zope.schema.vocabulary import SimpleVocabulary
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema
from emas.theme import MessageFactory as _

class IEmasUserDataSchema(IUserDataSchema):
    # Credits stored as an integer
    credits = Int(
        title=_(u'credits', default=u'Credits'),
        description=_(u'help_company', default=u"Credits a user can use towards paid services."),
        default=0,
        required=False)

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return IEmasUserDataSchema
