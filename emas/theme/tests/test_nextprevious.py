import os
import unittest2 as unittest
from zope.component import queryAdapter
from zope.interface import directlyProvides, directlyProvidedBy

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from base import INTEGRATION_TESTING

from Products.ATContentTypes.interface import IATFolder
from plone.app.folder.folder import IATUnifiedFolder
from plone.app.layout.nextprevious.interfaces import INextPreviousProvider
from plone.app.layout.navigation.interfaces import INavigationRoot

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
        directlyProvides(book, directlyProvidedBy(book), INavigationRoot)

        structure = (('folder001', 'Folder', u'Folder 001'),
                     ('folder002', 'Folder', u'Folder 002'),
                     ('folder003', 'Folder', u'Folder 003'),
                    )
        for number, details in enumerate(structure):
            itemId, itemType, itemTitle = details
            id = book.invokeFactory(itemType, itemId, title=itemTitle)
            chapter = book[id]
            chapter.setNextPreviousEnabled(True)
            chapter.setExcludeFromNav(False)
            id = chapter.invokeFactory(
                'File',
                'file%s' %number,
                title=u'File %s' %number)
            item = chapter._getOb(id)
            item.setNextPreviousEnabled(True)
            item.setExcludeFromNav(False)
            chapter.setDefaultPage(id) 
        return book

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.book = self._createBook()
    
    def test_IATUnifiedFolder(self):
        assert IATUnifiedFolder.providedBy(self.book)
    
    def test_findNextPreviousAdapter(self):
        adapter = INextPreviousProvider(self.book)
        assert adapter is not None
    
    def test_nextpreviousEnabled(self):
        adapter = INextPreviousProvider(self.book)

        self.book.setExcludeFromNav(False)
        self.book.setNextPreviousEnabled(True)
        self.assertEqual(adapter.enabled, True)

        self.book.setExcludeFromNav(True)
        self.book.setNextPreviousEnabled(True)
        self.assertEqual(adapter.enabled, False)

        self.book.setExcludeFromNav(False)
        self.book.setNextPreviousEnabled(False)
        self.assertEqual(adapter.enabled, False)
    
    def test_getNextItem(self):
        adapter = INextPreviousProvider(self.book)
        items = self.book.objectValues()
        
        currentItem = items[0]
        nextItem = adapter.getNextItem(currentItem)
        self.assertEqual(nextItem['url'], items[1].absolute_url())

        currentItem = items[1]
        nextItem = adapter.getNextItem(currentItem)
        self.assertEqual(nextItem['url'], items[2].absolute_url())
    
    def test_getFirstItem(self):
        firstItem = self.book.objectValues()[0]
        adapter = INextPreviousProvider(self.book)
        self.assertEqual(
            firstItem, adapter.getFirstItem(), 'Incorrect first item')

    def test_getLastItem(self):
        items = self.book.objectValues()[:]
        items.reverse()
        lastItem = items[0]
        adapter = INextPreviousProvider(self.book)
        self.assertEqual(
            lastItem, adapter.getLastItem(), 'Incorrect last item')

    def test_isFirstItem(self):
        firstItem = self.book.objectValues()[0]
        adapter = INextPreviousProvider(self.book)
        self.assertEqual(
            firstItem, adapter.getFirstItem(), 'First item check failed.')

    def test_isLastItem(self):
        items = self.book.objectValues()[:]
        items.reverse()
        lastItem = items[0]
        adapter = INextPreviousProvider(self.book)
        self.assertEqual(
            lastItem, adapter.getLastItem(), 'Last item check failed.')

    def test_stopAtFirst(self):
        firstItem = self.book.objectValues()[0]
        adapter = INextPreviousProvider(self.book)
        prevItem = adapter.getPreviousItem(firstItem)
        self.assertEqual(prevItem, None)

    def test_nextItemExcludedFromNav(self):
        """ If 'excludedFromNav' is set, the adapter should ignore this item.
        """
        firstItem = self.book.objectValues()[0]
        secondItem = self.book.objectValues()[1]
        adapter = INextPreviousProvider(self.book)
        secondItem.setExcludeFromNav(True)
        adapter.getNextItem(firstItem)


