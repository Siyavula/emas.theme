""" Run this zctl script to initialise the newsletter subscription for
    current members.
"""
import sys
import transaction
from types import ListType

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

newsletters = portal._getOb('newsletters')
newsletter = newsletters._getOb('everything-news')
receivers = ListType(newsletter.ploneReceiverMembers)
skipped = []

count = 0
prop_name = 'subscribe_to_newsletter'

all_members = portal.portal_membership.listMembers()

non_mxit_members = []
for member in all_members:
    if member.getId().endswith('mxit.com'):
        continue
    non_mxit_members.append(member)

for member in non_mxit_members:
    count += 1

    memberid = member.getId()
    print "Initialising newsletter subscription for %s" % memberid

    if memberid in receivers:
        print 'Skipping:%s (already in subscribed).' % memberid
    else:
        propsheet = member.getPropertysheet('mutable_properties')
        propsheet.setProperty(member, prop_name, True)
        if memberid not in receivers:
            receivers.append(memberid)
        else:
            skipped.append(memberid)

    if count % 100 == 0:
        print '************************************************************'
        print 'Committing transaction.'
        transaction.commit()

newsletter.ploneReceiverMembers = receivers

transaction.commit()
