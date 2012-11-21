""" Run this zctl script to initialise the newsletter subscription for
    current members.
"""
import sys
import transaction

from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager

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

import pdb;pdb.set_trace()
newsletters = portal._getOb('newsletters')
newsletter = newsletters._getOb('everything_news')
receivers = set(newsletter.ploneReceiverMembers)
memberids = set(portal.portal_membership.listMemberIds())
new_receivers = receivers.union(memberids)
newsletter.ploneReceiverMembers = new_receivers

transaction.commit()
