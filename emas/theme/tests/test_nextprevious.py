import os
import unittest2 as unittest
from zope.component import queryAdapter

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from base import INTEGRATION_TESTING

from Products.ATContentTypes.interface import IATFolder
from plone.app.folder.folder import IATUnifiedFolder
from plone.app.layout.nextprevious.interfaces import INextPreviousProvider

dirname = os.path.dirname(__file__)

class TestNextPrevious(unittest.TestCase):
    """ Test the nextprevious adapter """
    layer = INTEGRATION_TESTING

    def _createBook(self):
        id = self.portal.invokeFactory(
            'Folder',
            'Maths',
            title=u"Maths Grade 10")
        book = self.portal._getOb(id)
        structure = (('folder001', 'Folder', u'Folder 001'),
                     ('folder002', 'Folder', u'Folder 002'),
                     ('folder003', 'Folder', u'Folder 003'),
                    )
        for number, details in enumerate(structure):
            itemId, itemType, itemTitle = details
            id = book.invokeFactory(itemType, itemId, title=itemTitle)
            chapter = book[id]
            chapter.invokeFactory(
                'File',
                'file%s' %number,
                title=u'File %s' %number)
        return book

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.book = self._createBook()
    
    def test_IATUnifiedFolder(self):
        assert IATUnifiedFolder.providedBy(self.book)
    
    def test_findNextPreviousAdapter(self):
        adapter = queryAdapter(
            self.book, INextPreviousProvider, 'emas.nextprevious')
        assert adapter is not None
    
    def test_nextpreviousEnabled(self):
        self.book.setExcludeFromNav(True)
        self.book.setNextPreviousEnabled(True)
        adapter = queryAdapter(
            self.book, INextPreviousProvider, 'emas.nextprevious')
        self.assertEqual(adapter.enabled, True)

        self.book.setExcludeFromNav(False)
        self.book.setNextPreviousEnabled(True)
        self.assertEqual(adapter.enabled, False)

        self.book.setExcludeFromNav(False)
        self.book.setNextPreviousEnabled(False)
        self.assertEqual(adapter.enabled, False)
    
    def test_getFirst(self):
        firstItem = self.book.objectValues()[0]
        adapter = queryAdapter(
            self.book, INextPreviousProvider, 'emas.nextprevious')
        nextItem = adapter.getNextItem(firstItem)
        secondItem = self.book.objectValues()[1]
        self.assertEqual(nextItem['url'], secondItem.absolute_url())
