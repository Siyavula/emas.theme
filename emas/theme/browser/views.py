import json
from datetime import datetime, timedelta, date
from zope.component import queryUtility, queryAdapter
from zope.component import createObject

from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.users.browser.personalpreferences import UserDataPanel
from upfront.shorturl.browser.views import RedirectView

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Archetypes.interfaces import IBaseContent
from Products.Archetypes.utils import shasattr
from Products.CMFPlone.PloneBatch import Batch
from Products.statusmessages.interfaces import IStatusMessage

from emas.theme.behaviors.annotatable import IAnnotatableContent
from emas.theme.interfaces import IEmasSettings, IEmasServiceCost
from emas.theme import MessageFactory as _

NULLDATE = date(1970, 01, 01)

ALLOWED_TYPES = ['Folder',
                 'rhaptos.xmlfile.xmlfile',
                 'rhaptos.compilation.section',
                 'rhaptos.compilation.compilation',
                ]


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

    def userId(self):
        return self.portal_state.member().getId()

class AnnotatorHelpViewlet(ViewletBase):
    """ Adds a help panel for the annotator. """
    index = ViewPageTemplateFile('annotatorhelp.pt')


class SearchView(BrowserView):
    """ Combine searching for shortcode and searchabletext
    """

    def __call__(self):
        searchtext = self.request.get('SearchableText')
        shortcodeview = RedirectView(self.context, self.request)
        target = shortcodeview.lookup(searchtext)
        if target:
            self.request.response.redirect(target)
        else:
            state = self.context.restrictedTraverse('@@plone_portal_state')
            root = state.navigation_root()
            search_url = '%s/search?SearchableText=%s' % (
                root.absolute_url(), searchtext)
            self.request.response.redirect(search_url)

class AnnotatorEnabledView(BrowserView):
    """ Return true if annotator should be enabled
    """
    def enabled(self):
        if IAnnotatableContent.providedBy(self.context):
            return IAnnotatableContent(self.context).enableAnnotations
            
        if not IBaseContent.providedBy(self.context):
            return False
        enabled = self.context.Schema().getField(
            'enableAnnotations').getAccessor(self.context)()
        return enabled and bool(self.request.get('HTTP_X_THEME_ENABLED', None))

    __call__ = enabled


class EmasUserDataPanel(UserDataPanel):
    def __init__(self, context, request):
        super(EmasUserDataPanel, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('credits')
        self.form_fields = self.form_fields.omit('askanexpert_registrationdate')
        self.form_fields = self.form_fields.omit('answerdatabase_registrationdate')
        self.form_fields = self.form_fields.omit('moreexercise_registrationdate')

class CreditsViewlet(ViewletBase):
    """ Adds a help panel for the annotator. """
    index = ViewPageTemplateFile('credits-viewlet.pt')

    @property
    def credits(self):
        member = self.context.restrictedTraverse(
            '@@plone_portal_state').member()
        return member.getProperty('credits', 0)

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
    def is_enabled(self, service):
        pmt = getToolByName(self.context, 'portal_membership')
        member = pmt.getAuthenticatedMember()
        regdate = member.getProperty(service)
        try:
            return regdate > NULLDATE and True or False
        except: 
            return False
    
    @property
    def ask_expert_enabled(self):
        return self.is_enabled('askanexpert_registrationdate')

    @property
    def answer_database_enabled(self):
        return self.is_enabled('answerdatabase_registrationdate')

    @property
    def more_exercise_enabled(self):
        return self.is_enabled('moreexercise_registrationdate')

class EmasTransactionView(BrowserView):
    def buyCredit(self, credits, description):
        assert credits > 0
        return self.createTransaction(credits, description)

    def buyService(self, credits, description):
        assert credits > 0
        return self.createTransaction(-credits, description)

    def createTransaction(self, credits, description):
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
        message = '%s was successful.' %self.servicename
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
        pmt = getToolByName(self.context, 'portal_membership')
        member = pmt.getAuthenticatedMember()
        regdate = member.getProperty(self.memberproperty)
        try:
            return regdate > NULLDATE and self.current_credits >= 0
        except:
            return False
    
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
        return regdate + timedelta(30)

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


class RegisterForMoreExerciseView(PayserviceRegistrationBase):
    
    formsubmit_token = 'emas.theme.registerformoreexercise.submitted'
    formfield = 'registerformoreexercise'
    servicename = 'More exercise'
    memberproperty = 'moreexercise_registrationdate'
    creditproperty = 'exerciseCost'


class RegisterToAskQuestionsView(PayserviceRegistrationBase):

    formsubmit_token = 'emas.theme.registertoaskquestions.submitted'
    formfield = 'registertoaskquestions'
    servicename = 'Ask questions'
    memberproperty = 'askanexpert_registrationdate'
    creditproperty = 'questionCost'


class RegisterToAccessAnswerDatabaseView(PayserviceRegistrationBase):

    formsubmit_token = 'emas.theme.registertoaccessanswerdatabase.submitted'
    formfield = 'registertoaccessanswerdatabase'
    servicename = 'Access answer database'
    memberproperty = 'answerdatabase_registrationdate'
    creditproperty = 'answerCost'

