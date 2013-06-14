from zope.schema import List, TextLine, Bool, Int, Float
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

    bulksms_premium_number = TextLine(
        title=_(u'BulkSMS premium number'),
        description=_(u'The user sends and SMS to this number in order to pay.'),
        required=False,
        default=u'08200722929001'
    )

    bulksms_send_username = TextLine(
        title=_(u'BulkSMS username'),
        description=_(u'Used to authenticate the BulkSMS comms.'),
        required=False,
        default=u'upfronttest'
    )

    bulksms_send_password = TextLine(
        title=_(u'BulkSMS send password'),
        description=_(u'Used to authenticate when sending SMS.'),
        required=False,
        default=u'12345'
    )

    bulksms_send_url = TextLine(
        title=_(u'BulkSMS sending destination URL'),
        description=_(u'We send messages to this URL in order to send a SMS.'),
        required=False,
        default=u'http://bulksms.2way.co.za:5567/eapi/submission/send_sms/2/2.0'
    )

    bulksms_receive_password = TextLine(
        title=_(u'BulkSMS receive password'),
        description=_(u'Used to authenticate when receiving SMS.'),
        required=False,
        default=u'12345'
    )

    annual_expiry_warning_threshold = Int(
        title=_('Annual expiry warning threshold'),
        description=_('Relevant to member services with a subscription period ',
                      'of 365 days or more. Indicates how many days before ',
                      'expiry of the service the expiry warning is shown.'),
        required=False,
        default=30
    )

    monthly_expiry_warning_threshold = Int(
        title=_('Monthly expiry warning threshold'),
        description=_('Relevant to member services with a subscription period ',
                      'of 30 days or less. Indicates how many days before ',
                      'expiry of the service the expiry warning is shown.'),
        required=False,
        default=7
    )


class IEmasServiceCost(Interface):
    """
    """
    practiceprice = Float(
        title=_('Cost of 1 year subscription to Practice service'),
        description=_('WARNING: Changing this value will update the price for ALL practice services in the Products and Services folder. This price is also used on the order form.'),
        required=False,
        default=0.0
    )

    textbookprice = Float(
        title=_('Cost of textbook'),
        description=_('WARNING: Changing this value will update the price for ALL textbook products in the Products and Services folder. This price is also used on the order form'),
        required=False,
        default=0.0
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


class IMemberServiceGroup(Interface):

    def __init__(self, groupname, expirydate=None, services=[]):
        pass
    
    def add_service(self, service):
        pass

    def get_services(self):
        pass
