import os
from lxml import etree, html

from zope.interface import implements

from Products.PortalTransforms.interfaces import ITransform
from Products.PortalTransforms.utils import log

dirname = os.path.dirname(__file__)

class cnxmlplus_to_cnxml:
    implements(ITransform)

    __name__ = "cnxmlplus_to_cnxml"
    inputs = ("application/cnxmlplus+xml",)
    output = "application/cnxml+xml"

    def name(self):
        return self.__name__

    def convert(self, orig, data, **kwargs):
        #cnxmldoc = etree.fromstring(orig)

        #xslt_root = etree.parse(os.path.join(dirname, 'xsl', 'cnxml2html.xsl'))
        #transform = etree.XSLT(xslt_root)
        #htmldoc = transform(cnxmldoc)
        #result = '<div>'
        ## only return html inside the body tag
        #for e in htmldoc.xpath('//xhtml:body/*',
        #                        namespaces={'xhtml':
        #                                    'http://www.w3.org/1999/xhtml'}):
        #    result += etree.tostring(e)
        #result += '</div>'
        #data.setData(result)
        return data


def register():
    return cnxmlplus_to_cnxml()
