import re
import urllib2
import os
import lxml.html
import HTMLParser
from asciimathml_wrapped import asciimathml
from xml.etree import ElementTree

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
            for entry in element.findall('.//entry'):
                shortcode = entry.find('shortcode').text
                contentNode = entry.find('todo-content')
                if contentNode is not None:
                    contentNode.tag = 'div'
                    contentNode.attrib['class'] = "field answer"
                    if (len(contentNode) > 0) or (contentNode.text is not None):
                        contentNode.insert(0, lxml.html.Element("label", {"class": "formQuestion"}))
                        contentNode[0].text = 'Answer:'
                        contentNode[0].tail = contentNode.text
                        contentNode.text = ''
                    content.append(lxml.html.tostring(contentNode))
                else:
                    url = entry.find('url')
                    content.append(self.getURLContent(url.text))
                if shortcode is not None:
                    shortcode = 'sc' + shortcode.strip()
                    if content[-1][:5] == '<div ':
                        content[-1] = content[-1][:5] + 'id="%s" '%shortcode + content[-1][5:]
                    else:
                        print "WARNING: Got FullMarks solution that doesn't start with \"<div \""
                        print content
            # build a shortcode tree to contain all the fetched content
            try:
                sctree = lxml.html.fromstring(''.join(content))
            except Exception, msg:
                # Squash exceptions so that page still renders; log
                # error and generate empty solution environment
                from lxml import etree
                LOGGER.info('ERROR while build FullMarks solutions')
                LOGGER.info('  element: ' + repr(etree.tostring(element)))
                LOGGER.info('  content: ' + repr(''.join(content)))
                sctree = lxml.html.fromstring('<div> </div>')
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
                LOGGER.info('ERROR: video without URL... deleting.')
                element.getparent().remove(element)
            elif 'mindset.co.za' in params['url']:
                # Mindset video
                embedString = '<div id="sc' + params.get('shortcode', 'NONE') + '" class="video"><embed src="http://www.mindset.co.za/learn/sites/all/modules/mindset_video/mediaplayer/player.swf" width="' + params.get('width', '300') + '" height="' + params.get('height', 245) + '" allowscriptaccess="always" allowfullscreen="true" flashvars="file=' + params['url'] + '"/>'
                if params.get('strong') is not None:
                    embedString += '<p>' + params['strong'] + '</p>'
                embedString += '</div>'
                element.getparent().replace(element, lxml.html.fromstring(embedString))
            elif 'youtube.com' in params['url']:
                # YouTube video
                embedString = '<div id="sc' + params.get('shortcode', 'NONE') + '" class="video"><iframe width="' + params.get('width', '420') + '" height="' + params.get('height', '315') + '" src="' + params.get('url') + '" frameborder="0" allowfullscreen> </iframe>'
                if params.get('strong') is not None:
                    embedString += '<p>' + params['strong'] + '</p>'
                embedString += '</div>'
                element.getparent().replace(element, lxml.html.fromstring(embedString))
            else:
                LOGGER.info('ERROR: do not know how to handle video URL (%s)... deleting.'%params['url'])
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
                LOGGER.info('ERROR: simulation without URL... deleting.')
                element.getparent().remove(element)
            elif element.find('embed') is not None:
                # Verbatim embed code
                embedNode = element.find('embed')
                embedString = embedNode.text
                embedString = '<div id="sc' + params.get('shortcode', 'NONE') + '" class="simulation">' + embedString
                if params.get('strong') is not None:
                    embedString += '<p>' + params['strong'] + '</p>'
                embedString += '</div>'
                element.getparent().replace(element, lxml.html.fromstring(embedString))
            elif 'phet.colorado.edu' in params['url']:
                # Phet simulation
                embedString = '<iframe width="' + params.get('width', '400') + '" height="' + params.get('height', '300') + '" src="' + params.get('url') + '" frameborder="0" allowfullscreen> </iframe>'
                embedString = '<div id="sc' + params.get('shortcode', 'NONE') + '" class="simulation">' + embedString
                if params.get('strong') is not None:
                    embedString += '<p>' + params['strong'] + '</p>'
                embedString += '</div>'
                element.getparent().replace(element, lxml.html.fromstring(embedString))
            else:
                LOGGER.info('ERROR: do not know how to handle simulation URL (%s)... deleting.'%params['url'])
                element.getparent().remove(element)

        # Embed presentation
        # <presentation>
        #   <title>Chapter summary</title>
        #   <shortcode>VPcyl</shortcode>
	#   <url>http://www.slideshare.net/slideshow/embed_code/11078077</url>
        # </presentation>
        for element in tree.xpath('//todo-presentation'):
            subNodes = {}
            params = {}
            for key in ['strong', 'shortcode', 'url', 'width', 'height']:
                subNodes[key] = element.find('.//' + key)
                if subNodes[key] is not None:
                    params[key] = subNodes[key].text
            if (params.get('url') is None) or (params['url'].lower() == 'todo'):
                LOGGER.info('ERROR: presentation without URL... deleting.')
                element.getparent().remove(element)
            elif element.find('embed') is not None:
                # Verbatim embed code
                embedNode = element.find('embed')
                embedString = embedNode.text
                embedString = '<div id="sc' + params.get('shortcode', 'NONE') + '" class="presentation">' + embedString
                if params.get('strong') is not None:
                    embedString += '<p>' + params['strong'] + '</p>'
                embedString += '</div>'
                element.getparent().replace(element, lxml.html.fromstring(embedString))
            elif 'www.slideshare.net' in params['url']:
                embedString = '<div style="width:' + params.get('width', '425') + 'px"><iframe src="' + params['url'] + '" width="' + params.get('width', '425') + '" height="' + params.get('height', '355') + '" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"> </iframe></div>'
                embedString = '<div id="sc' + params.get('shortcode', 'NONE') + '" class="presentation">' + embedString
                if params.get('strong') is not None:
                    embedString += '<p>' + params['strong'] + '</p>'
                embedString += '</div>'
                element.getparent().replace(element, lxml.html.fromstring(embedString))
            else:
                LOGGER.info('ERROR: do not know how to handle presentation URL (%s)... deleting.'%params['url'])
                element.getparent().remove(element)

        # Render boxes (used for calculator buttons)
        for element in tree.xpath('//todo-box'):
            element.tag = 'span'
            element.attrib['style'] = 'border: solid black 1px; padding-left: 2px; padding-right: 2px; margin-left: 2px; margin-right: 2px;'

        # Remove to-do notes
        import utils
        dummyNode = utils.create_node('dummy')
        for element in tree.xpath('//todo'):
            # Use function from utils rather than
            #    element.getparent().remove(element)
            # so that the tail of the <todo> element being removed is
            # preserved.
            utils.etree_replace_with_node_list(element.getparent(), element, dummyNode)

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
        todoResult = '<div class="field answer"><label class="formQuestion">Answer:</label><p>To-do.</p></div>'
        if shortURL.lower() == 'todo':
            result = todoResult
        else:
            LOGGER.info('Fetching url: %s'%shortURL)
            try:
                handle = urllib2.urlopen(shortURL)
                content = handle.read()

                element = lxml.html.fromstring(content)
                element.make_links_absolute(base_url="http://www.fullmarks.org.za")
                for mathnode in element.xpath('//span[@class="AMcontainer"]'):
                    if len(mathnode) == 0:
                        # Guard against <span class="AMcontainer"></span> that sometimes appears
                        continue
                    asciimath = mathnode[0].text
                    mathml = ElementTree.tostring(asciimathml.parse(asciimath))
                    mathml = mathml.replace('`', '')
                    mathml = lxml.html.fromstring(mathml)
                    mathml.tail = mathnode.tail
                    mathnode.getparent().replace(mathnode, mathml)
                    
                for answer in element.xpath(
                    '//div[@id="item"]/div[starts-with(@class,"field answer")]'):
                    result += lxml.html.tostring(answer, method='xml')
            except urllib2.HTTPError, msg:
                LOGGER.info('ERROR: ' + str(msg) + ', URL = ' + shortURL)
                result = todoResult
        return result


def register():
    return shortcodehtml_to_html()
