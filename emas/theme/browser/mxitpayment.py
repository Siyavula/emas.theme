from urllib import urlencode
from five import grok
from Acquisition import aq_inner

from zope.interface import Interface
from zope.component import queryUtility

from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

from emas.theme.interfaces import IEmasSettings

from pas.plugins.mxit.plugin import member_id
from pas.plugins.mxit.plugin import password_hash
from pas.plugins.mxit.plugin import USER_ID_TOKEN


EXAM_PAPERS_GROUP = "ExamPapers"

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

grok.templatedir('templates')


class MxitPaymentRequest(grok.View):
    """
        Mxit payment processor.
    """

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('mxitpaymentrequest')
    
    def update(self):
        self.base_url = 'http://billing.internal.mxit.com/Transaction/PaymentRequest'
        self.action = self.context.absolute_url() + '/@@mxitpaymentrequest'
        self.vendor_id = '1'

        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(IEmasSettings)
        self.transaction_reference = self.settings.order_sequence_number + 1
        self.settings.order_sequence_number = self.transaction_reference
        self.transaction_reference = '%04d' % self.transaction_reference

        self.callback_url = self.context.absolute_url() + '/mxitpaymentresponse'
        self.product_id = 'test product'
        self.product_name = 'test product'
        self.product_description = 'test description'
        self.moola_amount = 1
        self.currency_amount = 1

        # check if the current mxit member belongs to the ExamPapers group
        memberid = member_id(self.request.get(USER_ID_TOKEN))
        gt = getToolByName(context, 'portal_groups')
        group = gt.getGroupById(EXAM_PAPERS_GROUP)
        if memberid in group.getMemberIds():
            self.request.response.redirect('/papers')
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

    
    def update(self):
        """ Handle the mxit response
        """
        context = self.context
        request = self.request

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
            password = password_hash(context, memberid)

            pmt = getToolByName(context, 'portal_membership')
            member = pmt.getMemberById(memberid)
            if not member:
                member = pmt.addMember(memberid, password, 'Member', '')
                member = pmt.getMemberById(memberid)
            
            # now add the member to the correct group
            gt = getToolByName(context, 'portal_groups')
            gt.addPrincipalToGroup(member.getId(), EXAM_PAPERS_GROUP)

    def get_url(self):
        return self.base_url + '/papers'
