""" script to import topics trees
"""
import sys
import transaction
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager

from zope.app.component.hooks import setSite

from plone.dexterity.utils import createContent, addContentToContainer

try:
    portal_id = sys.argv[1]
    filename = sys.argv[2]
except IndexError:
    print ("Usage: <instancehome>/bin/instance run %s "
           "<plonesite> <filename>" % sys.argv[0])
    sys.exit(1)

app = makerequest.makerequest(app)
user = app.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(app.acl_users))

portal = app[portal_id]
setSite(portal)

topictreefolder = portal.community.topictrees

def getTopicWithLabel(topicObj, label):
    for obj in topicObj.objectValues():
        if obj.Title() == label:
            return obj
    newtopic = createContent('collective.topictree.topic', title=label)
    addContentToContainer(topicObj, newtopic)
    topicObj = topicObj[newtopic.id]
    return topicObj

for line in open(filename).readlines():
    parts = line.split('/')
    print "Importing %s" % line

    level = 0
    if parts:
        parts.reverse()
        topicObj = topictreefolder
        while parts:
            label = parts.pop().strip()
            topicObj = getTopicWithLabel(topicObj, label)

transaction.commit()
