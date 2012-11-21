from zope.schema import List, TextLine, Bool, Int
from zope.interface import Interface
from emas.theme import MessageFactory as _

class IEmasThemeLayer(Interface):
    """ Marker interface for emas.theme. """

class IEmasSettings(Interface):
    """ So we can store some settings related to this product and the
        annotator.
    """

    order_sequence_number = Int(
        title=_(u'Order sequence number'),
        description=_(u'Order sequence number.'),
        default=0,
        required=True
    )

    order_email_address = TextLine(
        title=_(u'Order Email Address'),
        description=_(u'The addres orders should be emailed to.'),
        required=True
    )

    order_phone_number = TextLine(
        title=_(u'Order Phone Number'),
        description=_(u'The number customers should phone if they have '
                       'queries'),
        required=True
    )

    accountid = TextLine(
        title=_(u'Account ID'),
        description=_(u'Define the account it to use with the annotator.'),
        required=True
    )
    
    store = TextLine(
        title=_(u'Annotator Storage'),
        description=_(u'Define the url where the annotator store can be found.'),
        required=True
    )

    bcc_address = TextLine(
        title=_(u'Annotator Notifier BCC address'),
        description=_(u"Define the email address that get's bcc'd when notification emails are sent."),
        required=True,
        default=u'info@siyavula.com'
    )

    creditcost = Int(
        title=_('Credit Cost'),
        description=_('The cost per credit in cents'),
        required=False,
        default=0
    )

    practiceurl = TextLine(
        title=_('Practice Service URL'),
        required=False,
    )

    vcs_url = TextLine(
        title=_(u'VCS URL'),
        description=_(u'The URL to which the VCS payment request is made.'),
        required=False,
    )

    vcs_terminal_id = TextLine(
        title=_(u'VCS Terminal ID'),
        description=_(u'Assigned by VCS. Unique identifier of the merchant.'),
        required=False,
    )

    vcs_md5_key = TextLine(
        title=_(u'VCS md5 key'),
        description=_(u'Used to validate to VCS that the source or the call',
                      ' is legitemate.'),
        required=False,
    )

    vcs_user_id = TextLine(
        title=_(u'VCS user id'),
        description=_(u'This user will be used to create the member services.'),
        required=False,
    )

    maths_newsletter = TextLine(
        title=_(u'Everything Maths Newsletter.'),
        description=_(u'A newsletter for all interested in maths topics.'),
        required=False,
        default=_(u'EverythingNews')
    )

    science_newsletter = TextLine(
        title=_(u'Everything Science Newsletter.'),
        description=_(u'A newsletter for all interested in science topics.'),
        required=False,
        default=_(u'EverythingNews')
    )

class IEmasServiceCost(Interface):
    """
    """
    questionCost = Int(
        title=_('Question Cost'),
        description=_('The cost in credits to use the service.'),
        required=False,
        default=0
    )

    answerCost = Int(
        title=_('Answer Cost'),
        description=_('The cost in credits to use the service.'),
        required=False,
        default=0
    )

    exerciseCost = Int(
        title=_('Exercise Cost'),
        description=_('The cost in credits to use the service.'),
        required=False,
        default=0
    )

    MXitVendorId = TextLine(
        title=_(u'MXit Vendor ID'),
        description=_(u'MXit vendor id. Used in moola payment requests.'),
        required=True
    )
    
    PastMathsExamPapersCost = Int(
        title=_('Past Maths Exam Papers Cost'),
        description=_('The cost in moola to access past maths exam papers.'),
        required=False,
        default=200
    )

    PastScienceExamPapersCost = Int(
        title=_('Past Science Exam Papers Cost'),
        description=_('The cost in moola to access past science exam papers.'),
        required=False,
        default=200
    )
