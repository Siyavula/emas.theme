import os
import unittest2 as unittest
from plone.app.testing import TEST_USER_ID
from base import INTEGRATION_TESTING


class TestQueue(unittest.TestCase):
    """ Test the queue """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_q(self):
        import pdb;pdb.set_trace()
        self.fail()
