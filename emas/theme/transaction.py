from zope.schema import Datetime, Int
from plone.directives import form, dexterity
from emas.theme import MessageFactory as _

class ITransaction(form.Schema):
    """ A transaction, a user either bought credits, or spent credits on a
       service. """

    amount = Int(
        title=_(u"The amount of the transaction"),
        required=True
    )

    balance = Int(
        title=_(u"The total amount of credits after the transaction"),
        required=True
    )
