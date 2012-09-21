import os
import sys
import datetime
import transaction
from Testing import makerequest
from Acquisition import aq_base, aq_inner, aq_parent
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import getToolByName

from zope.app.component.hooks import setSite

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

wftool = portal.portal_workflow

wfs = {}
for id in wftool.objectIds():
    wf = wftool.getWorkflowById(id)
    if hasattr(aq_base(wf), 'updateRoleMappingsFor'):
        wfs[id] = wf
portal = aq_parent(aq_inner(wftool))
count = wftool._recursiveUpdateRoleMappings(portal.questions, wfs)

transaction.commit()
