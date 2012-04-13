from zope.interface import implements
from zope.schema import Int, Choice, TextLine, Date, List
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

access_types = SimpleVocabulary([
    SimpleTerm(value=u'maths grade 10', title=_(u'Maths grade 10')),
    SimpleTerm(value=u'maths grade 11', title=_(u'Maths grade 11')),
    SimpleTerm(value=u'maths grade 12', title=_(u'Maths grade 12')),
    SimpleTerm(value=u'science grade 10', title=_(u'Science grade 10')),
    SimpleTerm(value=u'science grade 11', title=_(u'Science grade 11')),
    SimpleTerm(value=u'science grade 12', title=_(u'Science grade 12')),
    ])

class IEmasUserDataSchema(IUserDataSchema):
    # Credits stored as an integer
    credits = Int(
        title=_(u'questions', default=u'Questions'),
        description=_(u'help_questions',
                      default=u"Question balance for Expert Answers service"),
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

    askanexpert_registrationdate = Date(
        title=_(u"label_askanexpert_registrationdate",
                default="Ask an expert - registration date."),
        required=False,
    )

    answerdatabase_registrationdate = Date(
        title=_(u"label_answerdatebase_registrationdate",
                default="Answer datebase - registration date."),
        required=False,
    )

    moreexercise_registrationdate = Date(
        title=_(u"label_moreexercise_registrationdate",
                default="More exercise - registration date."),
        required=False,
    )

    answerdatabase_expirydate = Date(
        title=_(u"label_answerdatebase_expirydate",
                default="Answer datebase - expiry date."),
        required=False,
    )

    moreexercise_expirydate = Date(
        title=_(u"label_moreexercise_expirydate",
                default="More exercise - expiry date."),
        required=False,
    )

    intelligent_practice_access = List(
        title=_(u"label_intelligent_practice_access",
                default="Intelligent practice access."),
        value_type = Choice(vocabulary=access_types),
        required=False,
    )
    

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return IEmasUserDataSchema
