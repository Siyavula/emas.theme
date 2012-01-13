import urllib2
import os
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
        result = self.postProcess(self.process(orig))
        data.setData(result)
        return data

    def process(self, orig):
        tree = lxml.html.fromstring(orig)

        # Replace exercise shortcodes with solutions from fullmarks
        for element in tree.xpath('//shortcodes'):
            content = []
            # get all the content from the contained urls
            for url in element.findall('.//url'):
                content.append(self.getURLContent(url.text))
            # build a shortcode tree to contain all the fetched content
            sctree = lxml.html.fromstring(''.join(content))
            sctree.set('class', 'shortcode-content')
            element.getparent().replace(element, sctree)

        # Embed videos
        # <video>
        #   <title>The dissolving process</title> # NOTE: <title> gets mangled to <strong> by cnxml2html
        #   <shortcode>VPabz</shortcode>
        #   <url>http://www.mindset.co.za/resources//0000033849/0000053197/0000054557/The_dissolving_process.flv</url>
        #   <width>300</width>
        #   <height>245</height>
        # </video>
        for element in tree.xpath('//todo-video'):
            subNodes = {}
            params = {}
            for key in ['strong', 'shortcode', 'url', 'width', 'height']:
                subNodes[key] = element.find('.//' + key)
                if subNodes[key] is not None:
                    params[key] = subNodes[key].text
            if (params.get('url') is None) or (params['url'].lower() == 'todo'):
                print 'Warning: video without URL... deleting.'
                element.getparent().remove(element)
            elif 'mindset.co.za' in params['url']:
                # Mindset video
                embedString = '<div class="video"><embed src="http://www.mindset.co.za/learn/sites/all/modules/mindset_video/mediaplayer/player.swf" width="' + params.get('width', '300') + '" height="' + params.get('height', 245) + '" allowscriptaccess="always" allowfullscreen="true" flashvars="file=' + params['url'] + '"/>'
                if params.get('strong') is not None:
                    embedString += '<p>' + params['strong'] + '</p>'
                embedString += '</div>'
                element.getparent().replace(element, lxml.html.fromstring(embedString))
            elif 'youtube.com' in params['url']:
                # YouTube video
                embedString = '<div class="video"><iframe width="' + params.get('width', '420') + '" height="' + params.get('height', '315') + '" src="' + params.get('url') + '" frameborder="0" allowfullscreen> </iframe>'
                if params.get('strong') is not None:
                    embedString += '<p>' + params['strong'] + '</p>'
                embedString += '</div>'
                element.getparent().replace(element, lxml.html.fromstring(embedString))
            else:
                print 'Warning: do not know how to handle video URL (%s)... deleting.'%params['url']
                element.getparent().remove(element)

        # Embed simulations
        # <simulation>
        #   <title>The following simulation allows...</title>
        #   <shortcode>VPcyz</shortcode>
	#   <url>http://phet.colorado.edu/en/simulation/circuit-construction-kit-dc</url>
        # </simulation>
        for element in tree.xpath('//todo-simulation'):
            subNodes = {}
            params = {}
            for key in ['strong', 'shortcode', 'url', 'width', 'height']:
                subNodes[key] = element.find('.//' + key)
                if subNodes[key] is not None:
                    params[key] = subNodes[key].text
            if (params.get('url') is None) or (params['url'].lower() == 'todo'):
                print 'Warning: simulation without URL... deleting.'
                element.getparent().remove(element)
            elif 'phet.colorado.edu' in params['url']:
                # Phet simulation
                embedString = '<div class="simulation"><iframe width="' + params.get('width', '400') + '" height="' + params.get('height', '300') + '" src="' + params.get('url') + '" frameborder="0" allowfullscreen> </iframe>'
                if params.get('strong') is not None:
                    embedString += '<p>' + params['strong'] + '</p>'
                embedString += '</div>'
                element.getparent().replace(element, lxml.html.fromstring(embedString))
            else:
                print 'Warning: do not know how to handle simulation URL (%s)... deleting.'%params['url']
                element.getparent().remove(element)

        # Remove to-do notes
        for element in tree.xpath('//todo'):
            element.getparent().remove(element)

        return lxml.html.tostring(tree, method='xml')

    def postProcess(self, orig):
        # Fix up any HTML we don't like, that came out of cnxml2html.
        from lxml import etree

        # Remove annotation parts of MathML so as not to confuse MathJax.
        pos = 0
        while True:
            start = orig.find("<annotation-xml", pos)
            if start == -1:
                break
            substr = "</annotation-xml>"
            stop = orig.find(substr, start)
            assert stop != -1
            stop += len(substr)
            orig = orig[:start] + orig[stop:]
            pos = start

        # Remove the annoying "Media file:" labels.
        nsPrefix = "{http://www.w3.org/1999/xhtml}"
        dom = etree.fromstring(orig)
        def traverse(node):
            if (node.tag == nsPrefix + 'div') and (node.attrib.get('class') == 'media'):
                objectNode = node.find(nsPrefix + 'object')
                if objectNode is not None:
                    if (len(objectNode) > 2) and (objectNode[0].tag == nsPrefix + 'span') and (objectNode[0].attrib.get('class') == 'cnx_label') and (objectNode[1].tag == nsPrefix + 'a') and (objectNode[1].attrib.get('href') == ''):
                        del objectNode[0]
                        del objectNode[0]
            for child in node:
                traverse(child)
        traverse(dom)
        html = etree.tostring(dom)

        return html
   
    @ram.cache(cache_key)
    def getURLContent(self, shortURL):
        result = ''
        if shortURL.lower() == 'todo':
            result = '<div class="question">\n                \n                    <div class="field ArchetypesField-TextField" id="archetypes-fieldname-question">\n          \n      \n        \n          \n            \n      <label class="formQuestion"><span>Question</span>:</label>\n      \n      <br /><div class="" id="parent-fieldname-question">\n            <p>To-do.</p>\n            \n        </div>\n    \n    \n        \n      \n    \n    </div>\n                \n            </div>\n\n\n            \n                <div class="field answer">\n                    <label class="formQuestion">Answer:</label>\n                    <p>To-do.</p>\n                </div>\n            \n\n            \n\n\n            '
        else:
            LOGGER.info('Fetching url:%s' %shortURL)
            handle = urllib2.urlopen(shortURL)
            content = handle.read()
            element = lxml.html.fromstring(content)
            for question in element.xpath(
                    '//div[@id="item"]/div[@class="question"]'):
                result += lxml.html.tostring(question, method='xml')
            for answer in element.xpath(
                    '//div[@id="item"]/div[@class="field answer"]'):
                result += lxml.html.tostring(answer, method='xml')
        return result

def register():
    return shortcodehtml_to_html()

