import datetime
import logging
from urllib import urlencode
from five import grok
from Acquisition import aq_inner

from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager

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

from emas.app.order import MOOLA
from emas.app.browser.utils import practice_service_uuids
from emas.app.browser.utils import generate_verification_code
from emas.app.memberservice import MemberServicesDataAccess 

log = logging.getLogger('emas.mobiletheme')

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

        pmt = getToolByName(self.context, 'portal_membership')
        memberid = member_id(
            self.request.get(USER_ID_TOKEN.lower(),
                             self.request.get(USER_ID_TOKEN)
                            )
        )
        if not memberid:
            raise ValueError('No member id supplied.')
        member = pmt.getMemberById(memberid)
        if not member:
            password = password_hash(self.context, memberid)
            pmt.addMember(memberid, password, 'Member', '')
            member = pmt.getMemberById(memberid)
            # login as new member
            newSecurityManager(self.request, member)

        registry = queryUtility(IRegistry)
        self.emas_settings = registry.forInterface(IEmasSettings)
        self.transaction_reference = self.emas_settings.order_sequence_number +1
        self.emas_settings.order_sequence_number = self.transaction_reference
        self.transaction_reference = '%04d' % self.transaction_reference

        self.product_id = self.request.get('productId')
        try:
            self.product = self.products_and_services._getOb(self.product_id)
        except AttributeError:
            raise AttributeError(
                'Product with id %s not found' % self.product_id
                )
            
        self.product_name = self.product.title
        self.product_description = self.product.description
        
        # create an order for this member : product combination
        if self.product:
            portal = pps.portal()
            member_orders = portal['orders']

            props = {'id'            : self.transaction_reference, 
                     'title'         : self.transaction_reference,
                     'userid'        : memberid,
                     'payment_method': MOOLA,
                     }
            self.order= createContentInContainer(
                member_orders,
                'emas.app.order',
                False,
                **props
            )
            self.order = member_orders._getOb(self.transaction_reference)
            self.order.verification_code = generate_verification_code(self.order)
            self.order.manage_setLocalRoles(self.order.userid, ('Owner',))
                
            relation = create_relation(self.product.getPhysicalPath())
            item_id = self.order.generateUniqueId(type_name='orderitem')
            props = {'id'           : item_id,
                     'title'        : item_id,
                     'related_item' : relation,
                     'quantity'     : 1}
            order_item = createContentInContainer(
                self.order,
                'emas.app.orderitem',
                False,
                **props
            )
            order_item.manage_setLocalRoles(self.order.userid, ('Owner',))

            self.callback_url = \
                '%s/mxitpaymentresponse?productId=%s&order_number=%s&verification_code=%s' %(
                    self.context.absolute_url(),
                    self.product_id,
                    self.order.getId(),
                    self.order.verification_code
            )

        self.cost_settings = registry.forInterface(IEmasServiceCost)
        self.vendor_id = self.cost_settings.MXitVendorId
        self.moola_amount = self.product.amount_of_moola
        self.currency_amount = self.product.price
        url = '%s/%s' %(self.navroot.absolute_url(), self.product.access_path)
        
        # get all active services for this user
        service_uuids = practice_service_uuids(self.context)
        dao = MemberServicesDataAccess(self.context)
        memberservices = dao.get_member_services(service_uuids, memberid)
        active_services = [m.related_service.to_object for m in memberservices]

        # check if the currently requested one is in the list
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

        self.orders = self.portal._getOb('orders')
        order_number = self.request['order_number']
        self.order = self.orders._getOb(order_number)

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
            self.productid = request['productId']
            self.service = self.products_and_services._getOb(self.productid)

            memberid = member_id(
                self.request.get(USER_ID_TOKEN.lower(),
                                 self.request.get(USER_ID_TOKEN)
                                )
            )
            password = password_hash(context, memberid)
            pmt = getToolByName(context, 'portal_membership')
            member = pmt.getMemberById(memberid)
            if not member:
                pmt.addMember(memberid, password, 'Member', '')
                member = pmt.getMemberById(memberid)
            
            # login as member
            newSecurityManager(self.request, member)
            # now transition the order to paid
            wf = getToolByName(self.context, 'portal_workflow')
            status = wf.getStatusOf('order_workflow', self.order)
            if status['review_state'] != 'paid':
                wf.doActionFor(self.order, 'pay')
                self.order.reindexObject()

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
