import datetime
from urllib import urlencode
from five import grok
from Acquisition import aq_inner

from zope.interface import Interface
from zope.component import queryUtility
from z3c.relationfield.relation import create_relation

from plone.uuid.interfaces import IUUID
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer

from emas.theme.interfaces import IEmasSettings
from emas.theme.interfaces import IEmasServiceCost

from pas.plugins.mxit.plugin import member_id
from pas.plugins.mxit.plugin import password_hash
from pas.plugins.mxit.plugin import USER_ID_TOKEN

from emas.app.browser.utils import practice_service_uuids
from emas.app.browser.utils import member_services 

EXAM_PAPERS_URL = "past-exam-papers"

MATHS_EXAM_PAPERS_GROUP = "PastMathsExamPapers"
SCIENCE_EXAM_PAPERS_GROUP = "PastScienceExamPapers"
INTELLIGENT_PRACTICE_GROUP = ""

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
        self.products_and_services = pps.portal()._getOb('products_and_services')
        self.navroot = pps.navigation_root()
        self.base_url = 'http://billing.internal.mxit.com/Transaction/PaymentRequest'
        self.action = self.context.absolute_url() + '/@@mxitpaymentrequest'
        memberid = member_id(self.request.get(USER_ID_TOKEN))

        registry = queryUtility(IRegistry)
        self.emas_settings = registry.forInterface(IEmasSettings)
        self.transaction_reference = self.emas_settings.order_sequence_number +1
        self.emas_settings.order_sequence_number = self.transaction_reference
        self.transaction_reference = '%04d' % self.transaction_reference

        self.product_id = self.request.get('productId')
        self.product = self.products_and_services._getOb(self.product_id)
        self.product_name = self.product.title
        self.product_description = self.product.description
        self.callback_url = '%s/mxitpaymentresponse?productId=%s' %(
            self.context.absolute_url(),
            self.product_id
        )
        
        # create and order for this member : product combination
        if self.product:
            portal = pps.portal()
            member_orders = portal['orders']

            registry = queryUtility(IRegistry)
            settings = registry.forInterface(IEmasSettings)
            ordernumber = settings.order_sequence_number + 1
            settings.order_sequence_number = ordernumber

            ordernumber = '%04d' % ordernumber
            member_orders.invokeFactory(
                type_name='emas.app.order',
                id=ordernumber,
                title=ordernumber,
                userid=memberid
            )
            self.order = member_orders._getOb(ordernumber)
                
            relation = create_relation(self.product.getPhysicalPath())
            item_id = self.order.generateUniqueId(type_name='orderitem')
            self.order.invokeFactory(
                type_name='emas.app.orderitem',
                id=item_id,
                title=item_id,
                related_item=relation,
                quantity=1,
            )

        self.cost_settings = registry.forInterface(IEmasServiceCost)
        self.vendor_id = self.cost_settings.MXitVendorId

        self.moola_amount = self.product.amount_of_moola
        self.currency_amount = self.product.price

        # check if the current mxit member belongs to the ExamPapers group
        if not memberid:
            return self.render()

        url = '%s/%s' %(self.navroot.absolute_url(), self.product.access_path)
        
        # get all active services for this user
        service_uuids = practice_service_uuids(self.context)
        memberservices = member_services(self.context, service_uuids)
        active_services = [m.related_service.to_object for m in memberservices]

        # check if the currently requested on is in the list
        if self.product in active_services:
            return self.request.response.redirect(url)
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
        self.pps = self.context.restrictedTraverse('@@plone_portal_state')
        self.portal = self.pps.portal()
        self.products_and_services = self.portal._getOb('products_and_services')
        self.memberservices = self.portal._getOb('memberservices')
        self.navroot = self.pps.navigation_root()

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
            self.service = self.products_and_services._getOb(self.productid)
            password = password_hash(context, memberid)

            pmt = getToolByName(context, 'portal_membership')
            member = pmt.getMemberById(memberid)
            if not member:
                pmt.addMember(memberid, password, 'Member', '')
                member = pmt.getMemberById(memberid)
            
            memberservice = self.get_memberservice(self.service,
                                                   memberid,
                                                   self.memberservices,
                                                   self.portal)

            access_group = self.service.access_group
            if access_group:
                # now add the member to the correct group
                gt = getToolByName(context, 'portal_groups')
                gt.addPrincipalToGroup(member.getId(), access_group)
                member = pmt.addMember(memberid, password, 'Member', '')
                member = pmt.getMemberById(memberid)
            
            # find the order and transition it to 'paid'
            
            # now add the member to the correct group
            gt = getToolByName(context, 'portal_groups')
            # at this stage group and productid are the same
            gt.addPrincipalToGroup(member.getId(), self.productid)

    def get_url(self):
        return '%s/%s' %(self.navroot.absolute_url(), self.service.access_path)

    def get_memberservice(self, service, memberid, memberservices, portal):
        now = datetime.datetime.now().date()
        pms = getToolByName(portal, 'portal_membership')
        pc = getToolByName(portal, 'portal_catalog')
        query = {'portal_type': 'emas.app.memberservice',
                 'serviceuid': IUUID(service),
                 'userid': memberid,
                }
        brains = pc(query)

        if len(brains) > 0:
            ms = brains[0].getObject()
        else:
            service_relation = create_relation(service.getPhysicalPath())
            mstitle = '%s for %s' % (service.title, memberid)
            props = {'title': mstitle,
                     'userid': memberid,
                     'related_service': service_relation,
                     'service_type': service.service_type}

            ms = createContentInContainer(
                memberservices,
                'emas.app.memberservice',
                False,
                **props
            )
            pms.setLocalRoles(ms, [memberid], 'Owner')

        if service.service_type == 'credit':
            credits = ms.credits
            credits += service.amount_of_credits
            ms.credits = credits
        elif service.service_type == 'subscription':
            if now > ms.expiry_date:
                ms.expiry_date = now
            expiry_date = ms.expiry_date + datetime.timedelta(
                service.subscription_period
            )
            ms.expiry_date = expiry_date

        ms.reindexObject()
        return ms
