""" Run this zctl script to initialise the registration property for all
    members
"""
import os
import sys
import transaction
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ModifyPortalContent
from Products.ATContentTypes.content.folder import ATFolder

from zope.app.component.hooks import setSite

from emas.theme.browser.views import NULLDATE

try:
    portal_id = sys.argv[1]
except IndexError:
    portal_id = 'Plone' 

if not app.hasObject(portal_id):
    print "Please specify the id of your plone site as the first argument "
    print "to this script."
    print "Usage: <instancehome>/bin/instance run %s <id>" % sys.argv[0]
    sys.exit(1)

portal = app[portal_id]
setSite(portal)

# we assume there is an admin user
app = makerequest.makerequest(app)
user = app.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(app.acl_users))

for member in portal.portal_membership.listMembers():

    transactions = portal.transactions

    memberid = member.getId()

    if not memberid in transactions.objectIds():
        folder = ATFolder(memberid)
        transactions._setObject(memberid, folder)
        transactions.reindexObject()
        folder.manage_permission(ModifyPortalContent, roles=[], acquire=0)
        print "creating folder for ", memberid


transaction.commit()
