from zope.schema import List, TextLine, Bool
from zope.interface import Interface
from emas.theme import MessageFactory as _

class IEmasSettings(Interface):
    """ So we can store some settings related to this product and the
        annotator.
    """
    accountid = TextLine(
        title=_(u'Account ID'),
        description=_(u'Define the account it to use with the annotator.'),
        required=True
    );
    
    store = TextLine(
        title=_(u'Annotator Storage'),
        description=_(u'Define the url where the annotator store can be found.'),
        required=True
    );
