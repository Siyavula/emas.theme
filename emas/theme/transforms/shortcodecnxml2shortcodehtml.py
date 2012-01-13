import os

from zope.interface import implements

from Products.PortalTransforms.interfaces import ITransform
from Products.PortalTransforms.utils import log

from rhaptos.cnxmltransforms.cnxml2html import cnxml_to_html

dirname = os.path.dirname(__file__)

class shortcodecnxml_to_shortcodehtml(cnxml_to_html):
    implements(ITransform)

    __name__ = "shortcodecnxml_to_shortcodehtml"
    inputs = ("application/shortcodecnxml+xml",)
    output = "text/shortcodehtml"
    
    def convert(self, orig, data, **kwargs):
        return cnxml_to_html.convert(self, orig, data, **kwargs)

def register():
    return shortcodecnxml_to_shortcodehtml()

