import urllib2
import os
import BeautifulSoup
import lxml.html

from zope.interface import implements
from plone.memoize import ram

from Products.PortalTransforms.interfaces import ITransform
from Products.PortalTransforms.utils import log

from logging import getLogger

LOGGER = getLogger('%s:' % __name__)

dirname = os.path.dirname(__file__)

def cache_key(func, self, shortURL):
    return shortURL

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
        for element in tree.xpath('//shortcodes'):
            content = []
            # get all the content from the contained urls
            for url in element.findall('.//url'):
                content.append(self.getURLContent(url.text))
            # build a shortcode tree to contain all the fetched content
            sctree = lxml.html.fromstring(''.join(content))
            sctree.set('class', 'shortcode-content')
            element.getparent().replace(element, sctree)
        return lxml.html.tostring(tree)
   
    @ram.cache(cache_key)
    def getURLContent(self, shortURL):
        result = ''
        LOGGER.info('Fetching url:%s' %shortURL)
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
