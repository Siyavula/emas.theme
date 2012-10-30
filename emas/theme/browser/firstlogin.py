from five import grok
from zope.interface import Interface

grok.templatedir('templates')


class FirstLogin(grok.View):
    """ Confirm an order.
    """
    
    grok.context(Interface)
    grok.require('zope2.View')

    def practice_url(self):
        pps = self.context.restrictedTraverse('@@plone_portal_state')
        navroot = pps.navigation_root().absolute_url()
        return '%s/@@practice' % navroot
