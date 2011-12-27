import datetime
from email.Message import Message
from lxml import etree
from cStringIO import StringIO

from rwproperty import getproperty, setproperty

from zope.interface import implements
from zope.component import adapts
from zope.filerepresentation.interfaces import IRawWriteFile
from plone.rfc822 import initializeObjectFromSchemata
from plone.dexterity.filerepresentation import WriteFileBase
from plone.dexterity.utils import iterSchemata

from rhaptos.xmlfile.xmlfile import IXMLFile

nsmap = {
    'cnxml': 'http://cnx.rice.edu/cnxml',
    'md': 'http://cnx.rice.edu/mdml',
    }

class CNXMLWriteFile(WriteFileBase):
    """IRawWriteFile file adapter for CNXML files.
    """
    
    implements(IRawWriteFile)
    adapts(IXMLFile)

    def __init__(self, context):
        super(CNXMLWriteFile, self).__init__(context)
        self._file = StringIO()
    
    @getproperty
    def mimeType(self):
        return 'application/cnxml+xml'
    
    @getproperty
    def name(self):
        return self._name
    
    @setproperty
    def name(self, value):
        self._name = value
    
    def close(self):
        self._closed = True
        data = self._getStream().getvalue()
        tree = etree.fromstring(data)
        docinfo = tree.getroottree().docinfo
        msg = Message()
        for tagname, attrname in (('title', 'title'), 
                                  ('abstract', 'description'),
                                  ('created', 'created'),
                                  ('modified', 'modified')):
            elems = tree.xpath('//md:%s' % tagname, namespaces=nsmap)
            if not elems:
                continue
            msg[attrname] = elems[0].text
        msg.set_payload(data)
        initializeObjectFromSchemata(self.context, iterSchemata(self.context),
                                     msg, docinfo.encoding)

        self._getStream().close()

    def _getStream(self):
        return self._file
