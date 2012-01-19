from zope.interface import implements
from zope.schema import Int, Choice, TextLine
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema
from emas.theme import MessageFactory as _

roles = SimpleVocabulary([
    SimpleTerm(value=u'Learner', title=_(u'Learner')),
    SimpleTerm(value=u'Educator', title=_(u'Educator')),
    SimpleTerm(value=u'Curriculum specialist',
               title=_(u'Curriculum specialist')),
    SimpleTerm(value=u'Other', title=_(u'Other'))
    ])

provinces = SimpleVocabulary([
    SimpleTerm(value=u'Eastern Cape', title=_(u'Eastern Cape')),
    SimpleTerm(value=u'Free State', title=_(u'Free State')),
    SimpleTerm(value=u'Gauteng', title=_(u'Gauteng')),
    SimpleTerm(value=u'KwaZulu-Natal', title=_(u'KwaZulu-Natal')),
    SimpleTerm(value=u'Limpopo', title=_(u'Limpopo')),
    SimpleTerm(value=u'Mpumalanga', title=_(u'Mpumalanga')),
    SimpleTerm(value=u'Northern Cape', title=_(u'Northern Cape')),
    SimpleTerm(value=u'North West', title=_(u'North West')),
    SimpleTerm(value=u'Western Cape', title=_(u'Western Cape')),
    ])

class IEmasUserDataSchema(IUserDataSchema):
    # Credits stored as an integer
    credits = Int(
        title=_(u'credits', default=u'Credits'),
        description=_(u'help_company',
                      default=u"Credits a user can use towards paid services."),
        default=0,
        required=False)
    userrole = Choice(
        title=_(u"Role"),
        vocabulary=roles,
        required=False,
        )
    school = TextLine(
        title=_(u'label_school', default=u'School Name'),
        required=False,
        default=u"",
        )
    province = Choice(
        title=_(u"label_province", default=u'Province'),
        vocabulary=provinces,
        required=False,
        )

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return IEmasUserDataSchema
