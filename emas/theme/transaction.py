from zope.schema import Datetime, Int
from plone.directives import form, dexterity
from emas.theme import MessageFactory as _

class ITransaction(form.Schema):
    """ A transaction, a user either bought credits, or spent credits on a
       service. """

    time = Datetime(
        title=_(u"The date and time of the transaction")
    )

    amount = Int(
        title=_(u"The amount of the transaction")
    )
