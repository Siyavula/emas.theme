from zope.schema import List, TextLine, Bool, Int
from zope.interface import Interface
from emas.theme import MessageFactory as _

class IEmasThemeLayer(Interface):
    """ Marker interface for emas.theme. """

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

    creditcost = Int(
        title=_('Credit Cost'),
        description=_('The cost per credit in cents'),
        required=False,
        default=0
    );

class IEmasServiceCost(Interface):
    """
    """
    questionCost = Int(
        title=_('Question Cost'),
        description=_('The cost in credits to use the service.'),
        required=False,
        default=0
    )

    answerCost = Int(
        title=_('Answer Cost'),
        description=_('The cost in credits to use the service.'),
        required=False,
        default=0
    )

    exerciseCost = Int(
        title=_('Exercise Cost'),
        description=_('The cost in credits to use the service.'),
        required=False,
        default=0
    )
