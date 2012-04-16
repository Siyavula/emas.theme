from email.Utils import formataddr
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email import Encoders

from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from emas.theme.interfaces import IEmasSettings

class OrderForm(BrowserView):
    """ Order form
    """

    index = ViewPageTemplateFile('templates/order.pt')
    ordertemplate = ViewPageTemplateFile('templates/ordermailtemplate.pt')
    ordernotification = ViewPageTemplateFile('templates/ordernotification.pt')

    def __call__(self):
        if self.request.has_key('submit'):
            practice_subjects = self.request.get('practice_subjects')
            practice_grade = self.request.get('practice_grade')
            include_textbook = self.request.get('include_textbook') == 'yes'
            include_expert_answers = \
                self.request.get('include_expert_answers') == 'yes'
            totalcost = 0
            packages = []
            if practice_subjects in ('Maths', 'Science'):
                packages.append(u'1 year subscription to Intelligent '
                                  'Practice for %s %s' % (
                                practice_subjects, practice_grade))
                totalcost = 150
                if include_textbook:
                    packages.append(u'Printed textbook '
                                     'for %s %s' % (
                                     practice_subjects, practice_grade))
                    totalcost = 200

            elif practice_subjects == 'Maths,Science':
                packages.append(u'1 year subscription to Intelligent '
                                 'Practice for Maths and Science %s' % 
                                 practice_grade)
                totalcost = 250
                if include_textbook:
                    packages.append(u'Printed textbook for Maths and '
                                     'Science %s' % practice_grade)
                    totalcost = 350
                
            if include_expert_answers:
                packages.append(u'Expert answers to 10 of your questions')
                totalcost += 25

            self.totalcost = totalcost
            self.packages = packages
            state = self.context.restrictedTraverse('@@plone_portal_state')
            self.username = state.member().getId()
            registry = queryUtility(IRegistry)
            self.settings = registry.forInterface(IEmasSettings)
            ordernumber = self.settings.order_sequence_number + 1
            self.settings.order_sequence_number = ordernumber
            self.ordernumber = '%04d' % ordernumber

            self.send()

        return self.index()

    def ordersubmitted(self):
        return self.request.has_key('ordersubmitted')

    def send(self): 
        """ Send Invoice to recipients
        """
        state = self.context.restrictedTraverse('@@plone_portal_state')
        portal = state.portal()
        member = state.member()
        host = portal.MailHost
        encoding = portal.getProperty('email_charset')

        send_from_address = formataddr(
            ( 'Siyavula Education', self.settings.order_email_address )
        )
        
        send_to_address = formataddr((member.getProperty('fullname'),
                                      member.getProperty('email')))

        subject = 'Order from %s Website' % state.navigation_root_title()

        # Generate message and attach to mail message
        message = self.ordertemplate(
            fullname=member.getProperty('fullname'),
            sitename=state.navigation_root_title(),
            packages=self.packages,
            totalcost=self.totalcost,
            username=member.getId(),
            ordernumber=self.ordernumber,
            email=self.settings.order_email_address,
            phone=self.settings.order_phone_number
        )

        portal.MailHost.send(message, send_to_address, send_from_address,
                             subject, charset=encoding)

        subject = 'New Order placed on %s Website' % \
            state.navigation_root_title()

        # Generate order notification
        message = self.ordernotification(
            fullname=member.getProperty('fullname'),
            sitename=state.navigation_root_title(),
            packages=self.packages,
            totalcost=self.totalcost,
            username=member.getId(),
            ordernumber=self.ordernumber,
            email=self.settings.order_email_address,
            phone=self.settings.order_phone_number
        )

        # Siyavula's copy
        portal.MailHost.send(message, send_from_address, send_from_address,
                             subject, charset=encoding)
