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
        msg = Message()
        try:
            tree = etree.fromstring(data)
            docinfo = tree.getroottree().docinfo
            encoding = docinfo.encoding
            msg['Content-Type'] = self.mimeType
            if docinfo.system_url == \
                'http://cnx.rice.edu/cnxml/0.5/DTD/cnxml_mathml.dtd':
                nsmap = {
                    'cnxml': 'http://cnx.rice.edu/cnxml',
                    'md': 'http://cnx.rice.edu/mdml/0.4',
                    }
                xpath_attr_map = (('//cnxml:name', 'title'), 
                                ('//md:abstract', 'description'),
                                ('//md:created', 'created'),
                                ('//md:revised', 'modified'))
            else:
                nsmap = {
                    'cnxml': 'http://cnx.rice.edu/cnxml',
                    'md': 'http://cnx.rice.edu/mdml',
                    }
                xpath_attr_map = (('//md:title', 'title'), 
                                ('//md:abstract', 'description'),
                                ('//md:created', 'created'),
                                ('//md:revised', 'modified'))

            for xpath, attrname in xpath_attr_map:
                elems = tree.xpath(xpath, namespaces=nsmap)
                if not elems:
                    continue
                msg[attrname] = elems[0].text

        except etree.XMLSyntaxError:
            encoding = 'utf-8'

        msg.set_payload(data)
        initializeObjectFromSchemata(self.context, iterSchemata(self.context),
                                     msg, encoding)

        self._getStream().close()

    def _getStream(self):
        return self._file
