import urllib2
import os
import BeautifulSoup
import lxml.html

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
        tree = lxml.html.fromstring(orig)
        for element in tree.xpath('//shortcodes//url'):
            content = lxml.html.fromstring(self.getURLContent(element.text))
            element.getparent().replace(element, content)
        return lxml.html.tostring(tree)
   
    def getURLContent(self, shortURL):
        result = ''
        handle = urllib2.urlopen(shortURL)
        content = handle.read()
        element = lxml.html.fromstring(content)
        for question in element.xpath(
                '//div[@id="item"]/div[@class="question"]'):
            result += lxml.html.tostring(question)
        for answer in element.xpath(
                '//div[@id="item"]/div[@class="field answer"]'):
            result += lxml.html.tostring(answer)

        return result

def register():
    return shortcodehtml_to_html()
