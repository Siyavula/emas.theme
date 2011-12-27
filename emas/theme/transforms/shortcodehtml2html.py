import urllib2
import os
import BeautifulSoup
from xml.dom.minidom import parseString

from zope.interface import implements

from Products.PortalTransforms.interfaces import ITransform
from Products.PortalTransforms.utils import log


dirname = os.path.dirname(__file__)

class shortcodehtml_to_html:
    """ Convert HTML with embedded shortcodes to HTML with the full dereferenced
        content to which the shortcode pointed.
    """

    implements(ITransform)

    __name__ = "shortcodehtml_to_html"
    inputs = ("text/shortcodehtml",)
    output = "text/html"
    cnxmlNamespace = "http://cnx.rice.edu/cnxml"

    def name(self):
        return self.__name__

    def convert(self, orig, data, **kwargs):
        result = self.process(orig)
        data.setData(result)
        return data

    def process(self, orig):
        dom = parseString(orig)
        elements = dom.getElementsByTagName('shortcodes')
        for element in elements:
            content = self.getContent(element, dom)
            parent = element.parentNode
            parent.replaceChild(content, element)
        return dom.toxml()
   
    def getContent(self, element, dom):
        content = dom.createElement('div')
        entries = element.getElementsByTagName('entry')
        for entry in entries:
            for code in entry.getElementsByTagName('url'):
                url = code.firstChild.nodeValue
                if url:
                    tmpcontent = self.getURLContent(url)
                    if tmpcontent:
                        newelement = dom.createElement('div')
                        textnode = dom.createTextNode(tmpcontent)
                        newelement.appendChild(textnode)
                        content.appendChild(newelement)
        return content

    def getURLContent(self, shortURL):
        content = ''
        try:
            handle = urllib2.urlopen(shortURL)
            content = handle.read()
            html = BeautifulSoup.BeautifulSoup(content)
            content = html.find('div', id='content')
            content = content.text
        except urllib2.URLError as e:
            msg = ''
            if hasattr(e, 'reason'):
                msg = e.reason
            elif hasattr(e, 'code'):
                msg = e.code
            print('The call failed:%s' %msg)
            content = 'Content not found'
        return content

def register():
    return shortcodehtml_to_html()
