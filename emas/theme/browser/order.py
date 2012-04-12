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
                                    'Practice for %s' % practice_subjects)
                totalcost = 150
                if include_textbook:
                    packages.append(u'Printed textbook '
                                        'for %s' % practice_subjects)
                    totalcost = 200

            elif practice_subjects == 'Maths,Science':
                packages.append(u'1 year subscription to Intelligent '
                                    'Practice for Maths and Science')
                totalcost = 250
                if include_textbook:
                    packages.append(u'Printed textbook for Maths and Science')
                    totalcost = 350
                
            if include_expert_answers:
                packages.append(u'Expert answers 10 of your questions')
                totalcost += 25

            self.totalcost = totalcost
            self.packages = packages

        else:
            return self.index()
            
    def send(self): 
        """ Send Invoice to recipients
        """
        state = self.context.restrictedTraverse('@@plone_portal_state')
        portal = state.portal()
        member = state.member()
        host = portal.MailHost
        encoding = portal.getProperty('email_charset')

        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(IEmasSettings)

        send_from_address = formataddr(
            ( 'Siyavula Education', self.settings.order_email_address )
        )

        send_to_address = formataddr((member.fullname, member.email))

        subject = 'Order from Everything %s Website' % \
            state.navigation_root_title()

        # Generate message and attach to mail message
        message = self.ordertemplate(
            fullname=member.fullname,
            sitename='Everything %s' % state.navigation_root_title(),
            packages=self.packages,
            cost=self.totalcost,
            username=member.getId(),
            email=self.settings.order_email_address,
            phone=self.settings.order_phone_number
        )

        portal.MailHost.send(message, send_from_address, send_to_address,
                             subject)

