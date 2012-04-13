""" Run this zctl script to initialise the registration property for all
    members
"""
import os
import sys
import datetime
import transaction
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import getToolByName

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

# 30 days free trial with 2 questions
today = datetime.date.today()
trialend = today + datetime.timedelta(days=30)

intelligent_practice_access = (
    'maths grade 10',
    'maths grade 11',
    'maths grade 12',
    'science grade 10',
    'science grade 11',
    'science grade 12',
)

properties = {'askanexpert_registrationdate': today,
              'answerdatabase_registrationdate': today,
              'moreexercise_registrationdate': today,
              'moreexercise_expirydate': trialend,
              'answerdatabase_expirydate': trialend,
              'credits': 2,
              'intelligent_practice_access': intelligent_practice_access,
              'trialuser': True,
              }

for member in portal.portal_membership.listMembers():

    print "Initialising regdate for ", member.getId()
    propsheet = member.getPropertysheet('mutable_properties')
    for key, value in properties.items():
        propsheet.setProperty(member, key, value)

transaction.commit()
