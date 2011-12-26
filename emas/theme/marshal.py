from lxml import etree
from cStringIO import StringIO

from rwproperty import getproperty, setproperty

from zope.interface import implements
from zope.component import adapts
from zope.filerepresentation.interfaces import IRawWriteFile
from plone.dexterity.filerepresentation import WriteFileBase

from rhaptos.xmlfile.xmlfile import IXMLFile

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
        self._getStream().close()
        import pdb; pdb.set_trace()
        doc = etree.fromstring(data)
         

    def _getStream(self):
        return self._file
