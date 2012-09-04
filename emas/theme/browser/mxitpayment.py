from urllib import urlencode
from five import grok
from Acquisition import aq_inner

from zope.interface import Interface
from zope.component import queryUtility

from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

from emas.theme.interfaces import IEmasSettings
from emas.theme.interfaces import IEmasServiceCost

from pas.plugins.mxit.plugin import member_id
from pas.plugins.mxit.plugin import password_hash
from pas.plugins.mxit.plugin import USER_ID_TOKEN


EXAM_PAPERS_URL = "past-exam-papers"

MATHS_EXAM_PAPERS_GROUP = "PastMathsExamPapers"
SCIENCE_EXAM_PAPERS_GROUP = "PastScienceExamPapers"

SUBJECT_MAP = {
    'maths': MATHS_EXAM_PAPERS_GROUP,
    'science': SCIENCE_EXAM_PAPERS_GROUP,
}

MXIT_MESSAGES = {
    '0':
        u'Transaction completed successfully.',

    '1':
        u'Transaction rejected by user.',

    '2':
        u'Invalid MXit login name or password (authentication failure).',

    '3':
        u'User account is locked.',

    '4':
        u'User has insufficient funds.',

    '5':
        u'Transaction timed out before a response was received from the user.',

    '6': 
        u'The user logged out without confirming or rejecting the transaction.',

    '-2':
        u'The transaction parameters are not valid.',

    '-1':
        u'Technical system error occurred.',
}


def getGroupName(navroot):
    subject = getSubject(navroot)
    return SUBJECT_MAP[subject]


def getProductId(navroot):
    subject = getSubject(navroot)
    return SUBJECT_MAP[subject]


def getSubject(navroot):
    return navroot.getId()


grok.templatedir('templates')


class MxitPaymentRequest(grok.View):
    """
        Mxit payment processor.
    """

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('mxitpaymentrequest')
     
    def update(self):
        pps = self.context.restrictedTraverse('@@plone_portal_state')
        self.navroot = pps.navigation_root()
        self.base_url = 'http://billing.internal.mxit.com/Transaction/PaymentRequest'
        self.action = self.context.absolute_url() + '/@@mxitpaymentrequest'

        registry = queryUtility(IRegistry)
        self.emas_settings = registry.forInterface(IEmasSettings)
        self.transaction_reference = self.emas_settings.order_sequence_number +1
        self.emas_settings.order_sequence_number = self.transaction_reference
        self.transaction_reference = '%04d' % self.transaction_reference

        self.product_id = self.request.get('productId')
        self.product_name = self.product_id
        self.product_description = self.product_id
        self.callback_url = '%s/mxitpaymentresponse?productId=%s' %(
            self.context.absolute_url(),
            self.product_id
        )

        self.cost_settings = registry.forInterface(IEmasServiceCost)
        self.vendor_id = self.cost_settings.MXitVendorId
        # get the schema for this record
        schema = self.cost_settings.__schema__
        # the the field by name from the schema
        field = schema[self.product_id + 'Cost']
        # get the value from the object 'cost_settings' via the field
        self.moola_amount = field.get(self.cost_settings)
        self.currency_amount = 1

        # check if the current mxit member belongs to the ExamPapers group
        memberid = member_id(self.request.get(USER_ID_TOKEN))
        if not memberid:
            return self.render()
        gt = getToolByName(self.context, 'portal_groups')
        group = gt.getGroupById(self.product_id)
        if memberid in group.getMemberIds():
            url = '%s/%s' %(self.navroot.absolute_url(), EXAM_PAPERS_URL)
            self.request.response.redirect(url)
        else:
            return self.render()

    def get_url(self):
        query_dict = {
            "VendorId": self.vendor_id,
            "TransactionReference": self.transaction_reference,
            "CallbackUrl": self.callback_url,
            "ProductId": self.product_id,
            "ProductName": self.product_name,
            "ProductDescription": self.product_description,
            "MoolaAmount": self.moola_amount,
            "CurrencyAmount": self.currency_amount,
        }
        return self.base_url + '?' + urlencode(query_dict)


class MxitPaymentResponse(grok.View):
    """
        Mxit payment processor.
    """
    
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('mxitpaymentresponse')


    def _mxitprofile(self, data):
        """ mxit profile data looks like this:
            'en,ZA,1975-10-29,Male,1' 
        """
        data = data.split(',')
        if len(data) > 4:
            return [data[1], data[2], data[3]]
        else:
            return ['', '', '']


    def update(self):
        """ Handle the mxit response
        """
        context = self.context
        request = self.request
        pps = self.context.restrictedTraverse('@@plone_portal_state')
        self.navroot = pps.navigation_root()

        self.base_url = context.absolute_url()
        self.response_code = request.get('mxit_transaction_res', None)
        # we try to interpret the response, if that fails we use the response
        # code itself as the message. That way we can at least see what we did
        # not understand :)
        self.message = MXIT_MESSAGES.get(self.response_code, self.response_code)

        # check response code
        if not self.response_code:
            return
       
        # Transaction completed successfully.
        if self.response_code == '0':
            memberid = member_id(request.get(USER_ID_TOKEN))
            self.productid = request['productId']
            password = password_hash(context, memberid)

            pmt = getToolByName(context, 'portal_membership')
            member = pmt.getMemberById(memberid)
            if not member:
                password = password_hash(context, memberid)
                country, birthdate, gender = \
                    self._mxitprofile(request.get('HTTP_X_MXIT_PROFILE', '')
                props={'fullname': request.get('HTTP_X_MXIT_NICK', ''),
                       'location': request.get('HTTP_X_MXIT_LOCATION', ''),
                       'language': request.get('LANGUAGE', ''),
                       'trialuser': True,
                       'ua_pixels': request.get('HTTP_UA_PIXELS', ''),
                       'ua_device': request.get('HTTP_X_DEVICE_USER_AGENT', ''),
                       'mxitcontact':  request.get('HTTP_X_MXIT_CONTACT', ''),
                       'country': country,
                       'birthdate': birthdate,
                       'gender': gender,
                       }
                member = pmt.addMember(memberid, password, 'Member', '', props)
                member = pmt.getMemberById(memberid)
            
            # now add the member to the correct group
            gt = getToolByName(context, 'portal_groups')
            # at this stage group and productid are the same
            gt.addPrincipalToGroup(member.getId(), self.productid)

    def get_url(self):
        return '%s/%s/@@list-exam-papers' %(
            self.navroot.absolute_url(), EXAM_PAPERS_URL)
