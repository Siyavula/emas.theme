# -*- extra stuff goes here -*-

from zope.i18nmessageid import MessageFactory
MessageFactory = MessageFactory('emas.theme')

from Products.EasyNewsletter.content.EasyNewsletter import schema

schema['ploneReceiverMembers'].widget.visible = {'view': 'invisible',
                                                 'edit': 'invisible'}

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
