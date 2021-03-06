import json
import hashlib
from datetime import datetime, timedelta, date
from DateTime import DateTime
from Acquisition import aq_inner
from AccessControl import getSecurityManager

from zope.component import queryUtility, queryAdapter, getMultiAdapter
from zope.component import createObject
from z3c.relationfield.relation import create_relation

from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.registry.interfaces import IRegistry
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.users.browser.personalpreferences import UserDataPanel
from plone.app.users.browser.personalpreferences import PasswordAccountPanel \
    as BasePasswordAccountPanel

from upfront.shorturl.browser.views import RedirectView

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ModifyPortalContent
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Archetypes.interfaces import IBaseContent
from Products.Archetypes.utils import shasattr
from Products.CMFPlone.PloneBatch import Batch
from Products.statusmessages.interfaces import IStatusMessage

from siyavula.what.browser.views import AddQuestionView as AddQuestionBaseView
from siyavula.what.browser.views import DeleteQuestionView as \
    DeleteQuestionBaseView 

from emas.app.browser.utils import member_credits
from emas.app.browser.utils import practice_service_intids
from emas.app.memberservice import MemberServicesDataAccess

from emas.theme.behaviors.annotatable import IAnnotatableContent
from emas.theme.interfaces import IEmasSettings, IEmasServiceCost
from emas.theme.browser.practice import IPracticeLayer

from emas.theme import MessageFactory as _

NULLDATE = date(1970, 01, 01)

ALLOWED_TYPES = ['Folder',
                 'rhaptos.xmlfile.xmlfile',
                 'rhaptos.compilation.section',
                 'rhaptos.compilation.compilation',
                ]

ANSWER_DATABASE = 'Access answer database'
PRACTICE_SYSTEM = 'Access exercise content'
ASK_QUESTIONS = 'Ask questions'
SUBSCRIPTION_PERIOD = 30        #this value is specified in days

SERVICE_MEMBER_PROP_MAP = {
    ANSWER_DATABASE: 'answerdatabase_expirydate',
    PRACTICE_SYSTEM: 'moreexercise_expirydate',
    ASK_QUESTIONS: 'askanexpert_expirydate'
}

HOST_NAME_MAP = {'maths'  : 'everythingmaths.co.za',
                 'science': 'everythingscience.co.za',
                }


def is_expert(context):
    # If the current user has 'siyavula.what.AddAnswer' permission
    # on the context they are considered experts and don't have to
    # register to use the payservices.
    permission = 'Siyavula What: Add Answer'
    pmt = getToolByName(context, 'portal_membership')
    return pmt.checkPermission(permission, context) and True or False


def vcs_hash(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

class EmasSettingsForm(RegistryEditForm):
    schema = IEmasSettings
    label = _(u'EMAS Settings')
    description = _(u"Use the settings below to configure "
                    u"emas.theme for this site")

class EmasControlPanel(ControlPanelFormWrapper):
    form = EmasSettingsForm


class EmasServiceCostsForm(RegistryEditForm):
    schema = IEmasServiceCost
    label = _(u'EMAS Service Cost')
    description = _(u"Configure the credit cost"
                    u" of the pay services.")
    
    def updateFields(self):
        super(EmasServiceCostsForm, self).updateFields()
    
    def updateWidgets(self):
        super(EmasServiceCostsForm, self).updateWidgets()

class EmasServiceCostControlPanel(ControlPanelFormWrapper):
    form = EmasServiceCostsForm

class AnnotatorConfigViewlet(ViewletBase):
    """ Adds a bit of javascript to the top of the page with details about
        the annotator. """
    index = ViewPageTemplateFile('annotatorconfig.pt')

    def update(self):
        super(AnnotatorConfigViewlet, self).update()
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(IEmasSettings)

    def accountId(self):
        return self.settings.accountid

    def annotatorStore(self):
        return self.settings.store

    def bccAddress(self):
        return self.settings.bcc_address
    
    def userId(self):
        return self.portal_state.member().getId()

class AnnotatorHelpViewlet(ViewletBase):
    """ Adds a help panel for the annotator. """
    index = ViewPageTemplateFile('annotatorhelp.pt')

class SearchView(BrowserView):
    """ Combine searching for shortcode and searchabletext
    """

    def __call__(self):
        searchtext = self.request.get('SearchableText', '')
        shortcodeview = RedirectView(self.context, self.request)
        target = shortcodeview.lookup(searchtext.strip())
        if target:
            self.request.response.redirect(target)
        else:
            state = self.context.restrictedTraverse('@@plone_portal_state')
            root = state.navigation_root()
            search_url = '%s/search?SearchableText=%s&search_came_from=%s' % (
                root.absolute_url(),
                searchtext,
                self.request.get('search_came_from', ''),
                )
            self.request.response.redirect(search_url)

class AnnotatorEnabledView(BrowserView):
    """ Return true if annotator should be enabled
    """
    def enabled(self):
        if IAnnotatableContent.providedBy(self.context):
            return IAnnotatableContent(self.context).enableAnnotations

        if not IBaseContent.providedBy(self.context):
            return False

        field = self.context.Schema().getField('enableAnnotations')
        if field is None:
            return False
        return field.getAccessor(self.context)()

    __call__ = enabled

class EmasUserDataPanel(UserDataPanel):

    template = ViewPageTemplateFile('templates/account-panel.pt')
    
    def __init__(self, context, request):
        super(EmasUserDataPanel, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('credits')
        self.form_fields = self.form_fields.omit('askanexpert_registrationdate')
        self.form_fields = self.form_fields.omit('answerdatabase_registrationdate')
        self.form_fields = self.form_fields.omit('moreexercise_registrationdate')
        self.form_fields = self.form_fields.omit('askanexpert_expirydate')
        self.form_fields = self.form_fields.omit('answerdatabase_expirydate')
        self.form_fields = self.form_fields.omit('moreexercise_expirydate')
        self.form_fields = self.form_fields.omit('intelligent_practice_access')
        self.form_fields = self.form_fields.omit('trialuser')

class CreditsViewlet(ViewletBase):
    """ Adds a help panel for the annotator. """
    index = ViewPageTemplateFile('credits-viewlet.pt')

    @property
    def credits(self):
        return member_credits(self.context)

class CreditsView(BrowserView):
    def __call__(self):
        amount = self.request.get('buy', None)
        if amount is not None:
            error, amount = self.validate(amount)
            if error:
                self.request['error'] = error
                return self.index()

            # XXX Payment gateway integration here, perhaps some utility we
            # can look up and delegate to.

            self.context.restrictedTraverse('@@emas-transaction').buyCredit(amount,
                "Credits purchased")
            IStatusMessage(self.request).addStatusMessage(_(u'Credit loaded.'))
            self.request['success'] = True

        return self.index()

    def buycredits(self):
        amount = self.request.get('buy', 0)
        error, amount = self.validate(amount)
        if error:
            raise ValueError(error)
        else:
            view = self.context.restrictedTraverse('@@emas-transaction')
            view.buyCredit(amount, "Credits purchased")
            msg = _(u'Credit loaded.')
            pps = self.context.restrictedTraverse('@@plone_portal_state')
            member = pps.member()
            credits = member.getProperty('credits')
            return json.dumps({'result': 'success',
                               'credits':credits,
                               'message': msg})

    def validate(self, amount):
        try:
            amount = int(amount)
        except ValueError:
            return _(u'Please enter an integer value'), 0
        if amount<=0:
            return _(u'Please enter a positive integer value'), 0
        return None, amount

    @property
    def cost(self):
        settings = queryUtility(IRegistry).forInterface(IEmasSettings)
        return settings.creditcost


class EnabledServicesView(BrowserView):
    """ Utility view to check and report on enabled pay services.
    """
    
    def get_member_services_for_subject(self, subject, memberid=None):
        """ This method probably needs caching since it is called a lot during
            the rendering of all pages which have the PremiumServicesViewlet.
        """
        services = {}
        portal_state = self.context.restrictedTraverse('@@plone_portal_state')
        if memberid is None:
            memberid = portal_state.member().getId()
        
        dao = MemberServicesDataAccess(self.context)
        memberid = member.getId()
        memberservices = dao.get_memberservices_by_subject(memberid, subject)
        for ms in memberservices:
            service = ms.related_service.to_object
            st = service.service_type
            details = {'service_title': service.Title(),
                       'grade': service.grade,
                       'expiry_date': ms.expiry_date,
                       'credits': ms.credits,}
            tmp_list = services.get(st, [])
            tmp_list.append(details)
            services[st] = tmp_list
        return services

    def is_enabled(self, service):
        if is_expert(self.context): return True

        now = date.today()
        try:
            memberprop = SERVICE_MEMBER_PROP_MAP.get(service)
            expirydate = self.expirydate(memberprop)
            # if there is no expiry date, the service has never been activated
            if not expirydate:
                return False 
            return now <= expirydate and True or False
        except: 
            return False

    def expirydate(self, memberprop):
        return memberservice_expiry_date(self.context) 
    
    def ask_expert_enabled(self, context=None):
        context = context or self.context

        if is_expert(context):
            return True
        
        current_credits = member_credits(context)
        return current_credits > 0

    def questions_left(self, context=None):
        context = context or self.context

        return member_credits(context)

    def answer_database_enabled(self, context=None):
        context = context or self.context

        if grade is None or subject is None:
            raise AttributeError('You must supply a grade and subject.')

        ps = self.context.restrictedTraverse('@@plone_portal_state')
        memberid = ps.member().getId()
            
        return self.is_enabled(ANSWER_DATABASE)

    def more_exercise_enabled(self, context=None):
        context = context or self.context

        permission = 'Manage portal'
        pmt = getToolByName(context, 'portal_membership')
        if pmt.checkPermission(permission, context):
            return True
        
        intids = practice_service_intids(context)
        ps = self.context.restrictedTraverse('@@plone_portal_state')
        memberid = ps.member().getId()
        dao = MemberServicesDataAccess(self.context)
        memberservices = dao.get_memberservices(intids, memberid)
        # if we cannot find any memberservices the exercise link should not be
        # available.
        if memberservices is None or len(memberservices) < 1:
            return False

        now = date.today()
        for ms in memberservices:
            if ms.expiry_date > now:
                return True
        
        return False

    @property
    def context_allows_questions(self):
        context = self.context
        allowQuestions = False
        if shasattr(context, 'allowQuestions'):
            allowQuestions = getattr(context, 'allowQuestions')
        return allowQuestions and context.portal_type in ALLOWED_TYPES


class EmasTransactionView(BrowserView):
    def buyCredit(self, credits, description):
        assert credits > 0
        return self.createTransaction(credits, description)

    def buyService(self, credits, description):
        assert credits > 0
        return self.createTransaction(-credits, description)

    def createTransaction(self, credits, description, tid=None):
        portal = self.context.restrictedTraverse(
            '@@plone_portal_state').portal()
        member = self.context.restrictedTraverse(
            '@@plone_portal_state').member()

        # Update our balance
        balance = member.getProperty('credits', 0)
        balance += credits
        member.setMemberProperties({'credits': balance})

        # Create a transaction entry
        transactionfolder = portal.transactions._getOb(member.getId())
        if tid is None:
            tid = self.context.generateUniqueId(type_name='Transaction')
        t = createObject('emas.theme.transaction', id=tid)
        now = datetime.now()
        t.title = now.strftime('%Y-%m-%d %H:%M:%S')
        t.description = description
        t.amount = credits
        t.effective = now
        t.balance = balance
        transactionfolder._setObject(tid, t)

    def balance(self):
        pps = self.context.restrictedTraverse('@@plone_portal_state')
        member = pps.member()
        return member.getProperty('credits', 0)

    def transactions(self):
        pps = self.context.restrictedTraverse('@@plone_portal_state')
        portal = pps.portal()
        member = pps.member()
        transactionfolder = portal.transactions._getOb(member.getId())

        # This will retrieve a Lazymap, it only fetches the item if it is
        # actually requested. Also, it retrieves it in tree order, and because
        # we use the date/time as the id, that means its in chronological
        # order. Neat, I hope?
        transactions = transactionfolder.objectValues()
        if transactions:
            b_start = self.request.get('b_start', 0)
            b_size = self.request.get('b_size', 20)
            return Batch(transactions, b_size, b_start)
        return None


class PayserviceRegistrationBase(BrowserView):

    """ Common ancestor for pay services views. """
    # these fields must be supplied by the inheriting classes.
    formsubmit_token = None
    formfield = None
    memberproperty = None

    def __call__(self):
        if self.request.form.get('form.button.submit', '').lower() == 'register':
            self.handleRegister()
        return self.index()
    
    def handleRegister(self):
        if self.request.form.get(self.formsubmit_token):
            enable_service = self.request.form.get(self.formfield)
            pmt = getToolByName(self.context, 'portal_membership')
            member = pmt.getAuthenticatedMember()
            regdate = NULLDATE
            if enable_service:
                regdate = date.today()
                member.setMemberProperties({self.memberproperty: regdate})
                view = self.context.restrictedTraverse('@@emas-transaction')
                transaction_message = 'Bought %s on %s' %(self.servicename, date.today())
                view.buyService(self.servicecost, transaction_message)
    
    def json_handleRegister(self):
        self.handleRegister()
        message = 'You successfully regsitered to %s.' %self.servicename.lower()
        if not self.is_registered:
            message = '%s was failed.' %self.servicename
        return json.dumps({'registered': self.is_registered,
                           'message': message,
                           'servicename': self.servicename,})

    @property
    def can_show(self):
        context = self.context
        allowQuestions = False
        if shasattr(context, 'allowQuestions'):
            allowQuestions = getattr(context, 'allowQuestions')
        return allowQuestions and context.portal_type in ALLOWED_TYPES

    @property
    def has_credits(self):
        return self.current_credits >= self.servicecost
    
    @property
    def is_registered(self):
        if self.is_expert: return True

        now = datetime.now()
        try:
            return now <= self.expirydate and self.current_credits > 0
        except:
            return False
    
    @property
    def is_expert(self):
        return is_expert(self.context)

    @property
    def servicecost(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IEmasServiceCost)
        servicecost = getattr(settings, self.creditproperty, 0)
        return servicecost

    @property
    def expirydate(self):
        pmt = getToolByName(self.context, 'portal_membership')
        member = pmt.getAuthenticatedMember()
        regdate = member.getProperty(self.memberproperty)
        if regdate == NULLDATE:
            regdate = date.today()
        return regdate + timedelta(SUBSCRIPTION_PERIOD)

    @property
    def current_credits(self):
        pmt = getToolByName(self.context, 'portal_membership')
        member = pmt.getAuthenticatedMember()
        current_credits = member.getProperty('credits', 0)
        return current_credits
        
    @property
    def cost(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IEmasSettings)
        return settings.creditcost

    @property
    def memberproperty(self):
        return SERVICE_MEMBER_PROP_MAP[self.servicename]

class RegisterForMoreExerciseView(PayserviceRegistrationBase):
    
    formsubmit_token = 'emas.theme.registerformoreexercise.submitted'
    formfield = 'registerformoreexercise'
    servicename = PRACTICE_SYSTEM
    creditproperty = 'exerciseCost'


class RegisterToAskQuestionsView(PayserviceRegistrationBase):

    formsubmit_token = 'emas.theme.registertoaskquestions.submitted'
    formfield = 'registertoaskquestions'
    servicename = ASK_QUESTIONS
    creditproperty = 'questionCost'

    def buyquestions(self):
        amount = self.request.get('buy', 0)
        error, amount = self.validate(amount)
        if error:
            raise ValueError(error)
        else:
            view = self.context.restrictedTraverse('@@emas-transaction')
            view.buyCredit(amount, "Questions purchased")
            msg = _(u'Payment successful and service activated.')
            pps = self.context.restrictedTraverse('@@plone_portal_state')
            member = pps.member()
            credits = member.getProperty('credits')
            return json.dumps({'result': 'success',
                               'credits':credits,
                               'message': msg})

    def startTransaction(self):
        quantity = self.request.get('quantity')
        error, quantity = self.validate(quantity)
        if error:
            raise ValueError(error)
        else:
            tid = self.context.generateUniqueId(type_name='Transaction')
            totalcost = self.servicecost * quantity
            pps = self.context.restrictedTraverse('@@plone_portal_state')
            description = self.servicename
            member = pps.member()
            settings = queryUtility(IRegistry).forInterface(IEmasSettings)
            vcs_terminal_id = settings.vcs_terminal_id
            md5key = settings.vcs_md5_key
            md5hash = vcs_hash(vcs_terminal_id + tid + description +
                               str(totalcost) + str(quantity) + md5key)
            return json.dumps({'vcs_terminal_id': vcs_terminal_id,
                               'transaction_id': tid,
                               'description': description,
                               'quantity': quantity,
                               'totalcost': totalcost,
                               'hash': md5hash})


    def validate(self, amount):
        try:
            amount = int(amount)
        except ValueError:
            return _(u'Please enter an integer value'), 0
        if amount<=0:
            return _(u'Please enter a positive integer value'), 0
        return None, amount

    @property
    def is_registered(self):
        if self.is_expert:
            return True

        return self.current_credits > 0
    

class RegisterToAccessAnswerDatabaseView(PayserviceRegistrationBase):

    formsubmit_token = 'emas.theme.registertoaccessanswerdatabase.submitted'
    formfield = 'registertoaccessanswerdatabase'
    servicename = ANSWER_DATABASE
    creditproperty = 'answerCost'

    @property
    def is_registered(self):
        if self.is_expert:
            return True

        now = datetime.now()
        try:
            return now <= self.expirydate
        except:
            return False


class PurchaseApproved(BrowserView):
    """ A credit card transaction was approved
    """

    def __call__(self):
        settings = queryUtility(IRegistry).forInterface(IEmasSettings)
        vcs_terminal_id = settings.vcs_terminal_id
        md5key = settings.vcs_md5_key

        vcsid = self.request.get('p1')
        assert vcsid == vcs_terminal_id

        tid = self.request.get('p2')
        servicename = self.request.get('p3')
        totalcost = self.request.get('p4')
        quantity = self.request.get('m1')

        md5hash = vcs_hash(vcsid + tid + servicename +
                           totalcost + quantity + md5key)

        pmt = getToolByName(self.context, 'portal_membership')
        regdate = date.today()
        member = pmt.getAuthenticatedMember()
        member.setMemberProperties({self.memberproperty: regdate})
        view = self.context.restrictedTraverse('@@emas-transaction')
        transaction_message = 'Bought %s on %s' %(servicename, regdate)
        view.createTransaction(quantity, description, tid)

        self.servicename = servicename

        return self.index()

    @property
    def memberproperty(self):
        return SERVICE_MEMBER_PROP_MAP[self.servicename]


class CreditView(BrowserView):
    def getAuthedMemberCreditsJSON(self):
        credits = member_credits(self.context)
        return json.dumps({'credits': credits})


class RequireLogin(BrowserView):
    """ Override Plone's require_login script to traverse from
        NavigationRoot, not portal
    """

    def __call__(self):
        login = 'login'

        state = self.context.restrictedTraverse('@@plone_portal_state')
        portal = state.portal()
        root = portal
        for parent in self.context.aq_chain:
            if INavigationRoot.providedBy(parent):
                root = parent
                break

        if portal.portal_membership.isAnonymousUser():
            return root.restrictedTraverse(login)()
        else:
            return root.restrictedTraverse('insufficient_privileges')()


class AnsweredMessageView(BrowserView):

    @property
    def question(self):
        return self.context.aq_parent
    
    def related_content(self):
        return self.question.relatedContent.to_object

    def get_content_url(self, content):
        """ We try to use the correct domain based on the folder in which
            the content resides.
            We use the navigation root of the content passed in and the 
            constant HOST_NAME_MAP above to build the url.
            If we cannot match any entry in HOST_NAME_MAP we use the 
            HTTP_HOST value of the current request.
        """
        pps = content.restrictedTraverse('@@plone_portal_state')
        default_host = self.request.HTTP_HOST
        navroot = pps.navigation_root()
        host = HOST_NAME_MAP.get(navroot.getId(), default_host)
        path = '/'.join(content.getPhysicalPath()[3:])
        return 'http://%s/%s' %(host, path)


# customise panel to not show edit-bar
class PasswordAccountPanel(BasePasswordAccountPanel):

    template = ViewPageTemplateFile('templates/account-panel.pt')


class HomeView(BrowserView):
    """ Home Page Logic
    """

    def site_url(self):
        return getToolByName(self.context, 'portal_url')

    def site_absolute_url(self):
        return getToolByName(self.context, 'portal_url').absolute_url()

    def show_tour(self):
        """ show tour if annonymous or (logged in and signed up < 8 days ago)
        """
        mt = getToolByName(self.context, 'portal_membership')
        if mt.isAnonymousUser(): 
            return True
        else:
            user = mt.getAuthenticatedMember().getUserName()
            memberid = mt.getAuthenticatedMember().getId()
            member = mt.getMemberById(memberid)
            registration_date = member.getProperty('registrationdate')
            now = DateTime()
            delta = now - registration_date
            if delta >= 8:
                return False
            return True

    def welcome_message(self):
        """ return welcome message to logged in user
        """
        mt = getToolByName(self.context, 'portal_membership')
        user = mt.getAuthenticatedMember().getUserName()
        fullname = mt.getAuthenticatedMember().getProperty('fullname')
        if fullname == '':
            if len(user) > 15:                
                return user[0:14] + '..'  # show only 1st 15 chars of username
                                          # to prevent overflow, show truncation
            return user                                   
        else:
            if len(fullname.lstrip(' ').split(' ')[0]) > 14:
                return fullname.lstrip(' ').split(' ')[0][0:13] + '..'
            return fullname.lstrip(' ').split(' ')[0]

class CatalogueView(BrowserView):
    """ Textbook Catalogue
    """

    def site_absolute_url(self):
        return getToolByName(self.context, 'portal_url').absolute_url()


class SchoolProductsPricingView(BrowserView):
    """ Products & Pricing: Teachers and Schools
    """

    def site_url(self):
        return getToolByName(self.context, 'portal_url')


class IndividualProductsPricingView(BrowserView):
    """ Products & Pricing: Parents and Learners
    """

    def site_url(self):
        return getToolByName(self.context, 'portal_url')


class EMASPersonalBarView(ViewletBase):
    
    def __init__(self, context, request):
        super(ViewletBase, self).__init__(context, request)
        self.__parent__ = self.context.aq_parent
        self.context = context
        self.request = request
        self.view = self
        self.manager = None
    
    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        super(EMASPersonalBarView, self).update()
        context = aq_inner(self.context)

        context_state = getMultiAdapter((context, self.request),
                                        name=u'plone_context_state')

        sm = getSecurityManager()
        self.user_actions = context_state.actions('user')
        self.anonymous = self.portal_state.anonymous()

        if not self.anonymous:
            member = self.portal_state.member()
            userid = member.getId()

            if sm.checkPermission('Portlets: View dashboard', context):
                self.homelink_url = "%s/useractions" % self.navigation_root_url
            else:
                self.homelink_url = "%s/personalize_form" % (
                                        self.navigation_root_url)

            membership = getToolByName(context, 'portal_membership')
            member_info = membership.getMemberInfo(userid)
            # member_info is None if there's no Plone user object, as when
            # using OpenID.
            if member_info:
                fullname = member_info.get('fullname', '')
            else:
                fullname = None
            if fullname:
                self.user_name = fullname
            else:
                self.user_name = userid


class EMASPortalMessage(BrowserView):
    """ Very basic browser view to give us something to call from our edge
        side include macros.
    """    

    index = ViewPageTemplateFile('templates/portalmessage.pt')

    def __call__(self):
        self.messages = []
        if hasattr(self.context, 'plone_utils'):
            self.messages = self.context.plone_utils.showPortalMessages()
        return self.index()
