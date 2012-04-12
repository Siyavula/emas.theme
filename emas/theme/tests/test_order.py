import os
import unittest2 as unittest
from plone.app.testing import TEST_USER_ID
from base import INTEGRATION_TESTING

from AccessControl import getSecurityManager

class TestOrderForm(unittest.TestCase):
    """ Test the nextprevious adapter """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_orderform(self):
        orderform = self.portal.restrictedTraverse('@@order') 
        
        # render the form
        result = orderform()

        # place an order for maths only
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Maths"
        request["include_textbook"] = "no"
        request["include_expert_answers"] = "no"

        orderform()
        self.assertEqual(orderform.totalcost, 150)
        self.assertEqual(orderform.packages,
            [u'1 year subscription to Intelligent Practice for Maths'])

        # place an order for maths and textbook
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Maths"
        request["include_textbook"] = "yes"
        request["include_expert_answers"] = "no"

        orderform()
        self.assertEqual(orderform.totalcost, 200)
        self.assertEqual(orderform.packages,
            [u'1 year subscription to Intelligent Practice for Maths',
             u'Printed textbook for Maths'])

        # place an order for science and expert answers
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Science"
        request["include_textbook"] = "no"
        request["include_expert_answers"] = "yes"

        orderform()
        self.assertEqual(orderform.totalcost, 175)
        self.assertEqual(orderform.packages,
            [u'1 year subscription to Intelligent Practice for Science',
             u'Expert answers 10 of your questions'])


        # place an order for maths and science only
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Maths,Science"
        request["include_textbook"] = "no"
        request["include_expert_answers"] = "no"

        orderform()
        self.assertEqual(orderform.totalcost, 250)
        self.assertEqual(orderform.packages,
            [(u'1 year subscription to Intelligent Practice for '
                'Maths and Science')])

        # place an order for everything
        request = self.layer['request']
        request["submit"] = True
        request["practice_subjects"] = "Maths,Science"
        request["include_textbook"] = "yes"
        request["include_expert_answers"] = "yes"

        orderform()
        self.assertEqual(orderform.totalcost, 375)
        self.assertEqual(orderform.packages,
            [(u'1 year subscription to Intelligent Practice for '
                'Maths and Science'),
             u'Printed textbook for Maths and Science',
             u'Expert answers 10 of your questions',
            ])
