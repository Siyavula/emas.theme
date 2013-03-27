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

groups_tool = portal.portal_groups
group_id = "newsletter_subscribers"
if not group_id in groups_tool.getGroupIds():
    groups_tool.addGroup(group_id)
    portal.acl_users.source_groups.updateGroup(
        group_id, title="Newsletter Subscribers")

count = 0
prop_name = 'subscribe_to_newsletter'

for memberid in receivers:
    count += 1

    print "Adding %s" % memberid
    groups_tool.addPrincipalToGroup(memberid, group_id)

    if count % 100 == 0:
        print '************************************************************'
        print 'Committing transaction.'
        transaction.commit()

newsletter.ploneReceiverMembers = receivers

transaction.commit()
