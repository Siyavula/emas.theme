from zope.interface import implements
from zope.component import getMultiAdapter

from Acquisition import aq_inner
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.uuid.interfaces import IUUID
from plone.app.layout.viewlets.common import ViewletBase
from siyavula.what.browser.viewlets import QAViewlet as BaseQAViewlet
from webcouturier.dropdownmenu.browser import dropdown
from webcouturier.dropdownmenu.browser.interfaces import IDropdownMenuViewlet

from emas.theme.browser.views import is_expert
from emas.theme import MessageFactory as _


class QAViewlet(BaseQAViewlet):
    """ Specialise the siyavula.what viewlet to check if the service is enabled.
    """

    def questions(self):
        """ Return all questions that have the current context set
            as 'relatedContent'.

            If the user is not registered for the service, we still
            return all the questions (and answers) that he owns.
            That way, eventhough the service subscription has expired,
            the user still has access to the questions and answers
            for which he paid.
        """
        context = self.context
        uuid = IUUID(context)
        pc = getToolByName(context, 'portal_catalog')
        query = {'portal_type': 'siyavula.what.question',
                 'relatedContentUID': uuid,
                 'sort_on': 'created',
                }
        if is_expert(self.context):
            brains = pc(query)
            return brains and [b.getObject() for b in brains] or []

        view = self.context.restrictedTraverse('@@enabled-services')
        if not view.answer_database_enabled:
            pmt = getToolByName(self.context, 'portal_membership')
            member = pmt.getAuthenticatedMember()
            query['Creator'] = member.getId()
        brains = pc(query)
        return brains and [b.getObject() for b in brains] or []

    def allowQuestions(self):
        """ Check against the members enabled services.
        """
        context = self.context
        allowQuestions = False
        if shasattr(context, 'allowQuestions'):
            allowQuestions = getattr(context, 'allowQuestions')
        return allowQuestions

    def is_enabled(self):
        """
        """
        context = self.context
        view = context.restrictedTraverse('@@enabled-services')
        return view.ask_expert_enabled(self.context)

    def render(self):
        """ We render an empty string when a specific piece of content
            does not allow questions.
        """
        if self.allowQuestions():
            return super(QAViewlet, self).render()
        else:
            return ""


class DropdownMenuViewlet(dropdown.DropdownMenuViewlet):
    """ Specialise dropdown menu viewlet to render custom template for
        theme
    """
    implements(IDropdownMenuViewlet)

    _theme_template = ViewPageTemplateFile('templates/dropdown.pt')

    _default_template = ViewPageTemplateFile('templates/dropdown_sections.pt')

    def index(self):
        if self.request.get('HTTP_X_THEME_ENABLED') == True:
            return self._theme_template()
        else:
            # this template effectively disables dropdown in Plone's
            # default theme
            return self._default_template()

    def update(self):
        super(DropdownMenuViewlet, self).update()
        context = aq_inner(self.context)
        portal_state_view = getMultiAdapter((context, self.request),
                                             name='plone_portal_state')
        navroot = portal_state_view.navigation_root()
        self.site_url = navroot.absolute_url()

class MathJaxViewlet(ViewletBase):
    """ Viewlet to render Mathjax configuration inline
    """

    def index(self): 
        context = aq_inner(self.context)
        portal_state_view = getMultiAdapter((context, self.request),
                                             name='plone_portal_state')
        navroot = portal_state_view.navigation_root()
        return """\
<script type="text/x-mathjax-config">
MathJax.Ajax.timeout = 60*1000;
MathJax.Hub.Config({
    config: ["MMLorHTML.js"],
    extensions: ["tex2jax.js","mml2jax.js","MathZoom.js","MathMenu.js","toMathML.js","TeX/noErrors.js","TeX/noUndefined.js","TeX/AMSmath.js","TeX/AMSsymbols.js"],
    jax: ["input/TeX","input/MathML","output/HTML-CSS","output/NativeMML"]
});
</script>
<script type="text/javascript" src="%s/++resource++fullmarks.mathjax/mathjax/MathJax.js">
</script>
""" % navroot.absolute_url()


class PracticeServiceMessagesViewlet(ViewletBase):
    
    index = ViewPageTemplateFile('templates/practice_service_messages.pt')

    def render(self):
        return self.index()
