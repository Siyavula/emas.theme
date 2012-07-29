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

    vcs_terminal_id = TextLine(
        title=_('VCS Terminal ID'),
        required=False,
    )

    vcs_md5_key = TextLine(
        title=_('VCS md5 key'),
        required=False,
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
