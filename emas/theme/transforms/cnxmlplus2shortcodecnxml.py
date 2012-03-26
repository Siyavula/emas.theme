import os
from lxml import etree
import utils
import hashlib

from zope.interface import implements
from Products.PortalTransforms.interfaces import ITransform
from Products.PortalTransforms.utils import log

from logging import getLogger

LOGGER = getLogger('%s:' % __name__)

dirname = os.path.dirname(__file__)

class cnxmlplus_to_shortcodecnxml:
    """Convert CNXML+ down to CNXML
       traverse every element in tree, find matching environments, transform
    """

    implements(ITransform)

    __name__ = "cnxmlplus_to_shortcodecnxml"
    inputs = ("application/cnxmlplus+xml",)
    output = "application/shortcodecnxml+xml"

    def name(self):
        return self.__name__

    def convert(self, orig, data, **kwargs):
        result = self.process(orig)
        data.setData(result)
        return data

    def process(self, markup):
        # Convert down to CNXML

        # Strip comments
        pos = 0
        while True:
            start = markup.find('<!--', pos)
            if start == -1:
                break
            stop = markup.find('-->', start)
            assert stop != -1
            stop += 3
            markup = markup[:start] + markup[stop:]
            pos = start

        dom = etree.fromstring(markup)

        # Check for a pspicture generator version tag
        metadataNode = dom.find('metadata')
        self.pspictureGeneratorVersion = '1.0'
        if metadataNode is not None:
            generatorNode = metadataNode.find('pspicture-generator-version')
            if generatorNode is not None:
                self.pspictureGeneratorVersion = generatorNode.text.strip()

        # Strip out <section type="chapter">
        dom = dom.find('content')
        assert len(dom) == 1 # only a single chapter section
        assert (dom[0].tag == 'section') and (dom[0].attrib['type'] == 'chapter')
        chapterNode = dom[0]
        titleNode = chapterNode[0]
        assert titleNode.tag == 'title'
        contentsNodes = chapterNode[1:]
        del dom[0]
        dom.append(titleNode)
        dom.append(utils.create_node('content'))
        for node in contentsNodes:
            dom[-1].append(node)

        # Build chapter hash from title: for pspictures directory
        if titleNode.text is None:
            chapterTitle = ''
        else:
            chapterTitle = titleNode.text
        self.chapterHash = hashlib.md5(chapterTitle).hexdigest()
        #print 'hash:', self.chapterHash

        # Hack to replace shortcode content with todo-content.
        # traverse_dom_for_cnxml() needs to change eventually to use
        # xpath rather than a recursive function.
        for contentNode in dom.xpath('//shortcodes/entry/content'):
            contentNode.tag = 'todo-content'

        # Transform using new-style (xpath-based) transform
        self.transform(dom)

        # TOFIX: Remaining elements using old-style transform
        # Transform all elements in document, except pspictures
        self.traverse_dom_for_cnxml(dom)

        # Transform pspictures
        self.psPictureCount = 0
        self.tikzPictureCount = 0
        self.traverse_dom_for_pspictures(dom)

        markup = utils.declutter_latex_tags(etree.tostring(dom)).strip()
        assert markup[:8] == '<content'
        assert markup[-10:] == '</content>'
        markup = '<?xml version="1.0"?>\n<document xmlns="http://cnx.rice.edu/cnxml"' + markup[8:-10] + '</document>\n'
        return markup

    def pspicture_path(self, element):
        prefix = {
            'pspicture': 'ps',
            'tikzpicture': 'tikz',
        }[element.tag]
        if self.pspictureGeneratorVersion == '1.0':
            count = {
                'pspicture': self.psPictureCount,
                'tikzpicture': self.tikzPictureCount,
            }[element.tag]
            return prefix + 'pictures%s/%03i.png'%(self.chapterHash, count)
        elif self.pspictureGeneratorVersion == '1.1':
            code = ''.join(element.find('code').text.split())
            codeHash = hashlib.md5(code).hexdigest()
            return prefix + 'pictures/' + codeHash + '.png'
        else:
            raise ValueError, "Unknown pspicture generator version"

    def transform(self, dom):
        # Currency
        for currencyNode in dom.xpath('//currency'):
            latexMode = utils.etree_in_context(currencyNode, 'latex')
            currencyPrecision = int(currencyNode.attrib.get('precision', '2'))
            symbolNode = currencyNode.find('symbol')
            if symbolNode is None:
                symbol = 'R'
                symbolLocation = 'front'
            else:
                symbol = symbolNode.text.strip()
                symbolLocation = symbolNode.attrib.get('location', 'front')
            numberNode = currencyNode.find('number')
            numberNode.text = ("%%.%if"%currencyPrecision)%float(numberNode.text.strip())

            replacementNode = etree.Element('dummy')
            if symbolLocation == 'front':
                if latexMode:
                    replacementNode.text = r'\text{' + symbol + ' }'
                else:
                    replacementNode.text = symbol + u'\u00a0'
                replacementNode.append(numberNode)
            else:
                replacementNode.append(numberNode)
                if latexMode:
                    replacementNode.tail = r'\text{ ' + symbol + '}'
                else:
                    replacementNode.tail = u'\u00a0' + symbol
            utils.etree_replace_with_node_list(currencyNode.getparent(), currencyNode, replacementNode)

    def traverse_dom_for_pspictures(self, element):
        # <pspicture><code>
        if element.tag == 'pspicture':
            self.psPictureCount += 1
            src = self.pspicture_path(element)
            mediaNode = utils.create_node('media')
            mediaNode.append(utils.create_node('image'))
            mediaNode.attrib['alt'] = 'Image'
            mediaNode[0].attrib['src'] = src
            mediaNode.tail = element.tail
            element.getparent().replace(element, mediaNode)
        elif element.tag == 'tikzpicture':
            self.tikzPictureCount += 1
            src = self.pspicture_path(element)
            mediaNode = utils.create_node('media')
            mediaNode.append(utils.create_node('image'))
            mediaNode.attrib['alt'] = 'Image'
            mediaNode[0].attrib['src'] = src
            mediaNode.tail = element.tail
            element.getparent().replace(element, mediaNode)
        else:
            children = element.getchildren()
            for child in children:
                self.traverse_dom_for_pspictures(child)

    def traverse_dom_for_cnxml(self, element):
        # traverse every element in tree, find matching environments, transform
        for child in element:
            self.traverse_dom_for_cnxml(child)

        childIndex = 0
        while childIndex < len(element):
            child = element[childIndex]

            if child.tag in ['video', 'simulation', 'presentation', 'box']:
                child.tag = 'todo-' + child.tag
                childIndex += 1

            elif child.tag == 'image':
                # <image> <arguments/> <src/> </image>
                mediaNode = utils.create_node('media')
                mediaNode.append(utils.create_node('image'))
                mediaNode.attrib['alt'] = 'Image'
                urlNode = child.find('src')
                if urlNode is not None:
                    mediaNode[0].attrib['src'] = urlNode.text.strip()
                else:
                    mediaNode[0].attrib['src'] = ''
                mediaNode.tail = child.tail
                element[childIndex] = mediaNode
                childIndex += 1

            elif child.tag == 'figure':
                typeNode = child.find('type')
                if typeNode is not None:
                    typ = typeNode.text.strip()
                    child.attrib['type'] = typ
                    typeNode.tag = 'label'
                    typeNode.text = {'figure': 'Figure', 'table': 'Table'}[typ]
                childIndex += 1

            elif child.tag == 'caption':
                if (len(child) == 1) and (child[0].tag == 'para'):
                    utils.etree_replace_with_node_list(child, child[0], child[0])
                childIndex += 1

            elif child.tag == 'activity':
                # <activity type="activity"><title/> <section><title/>...</section> </activity>
                child.tag = 'example'
                child.append(utils.create_node('label', text={
                    'g_experiment': 'General experiment',
                    'f_experiment': 'Formal experiment',
                    'i_experiment': 'Informal experiment',
                    'activity': 'Activity',
                    'Investigation': 'Investigation',
                    'groupdiscussion': 'Group discussion',
                    'casestudy': 'Case study',
                    'project': 'Project'}[child.attrib['type']]))
                pos = 1
                while pos < len(child):
                    if child[pos].tag == 'section':
                        sectionNode = child[pos]
                        assert sectionNode[0].tag == 'title'
                        del child[pos]
                        child.insert(pos, utils.create_node('para'))
                        child[pos].append(utils.create_node('emphasis', text=sectionNode[0].text.strip()))
                        child[pos][-1].attrib['effect'] = 'bold'
                        pos += 1
                        sectionChildren = sectionNode.getchildren()
                        for i in range(1, len(sectionChildren)):
                            child.insert(pos, sectionChildren[i])
                            pos += 1
                    else:
                        pos += 1
                childIndex += 1

            elif child.tag == 'worked_example':
                # <worked_example> <title/> <question/> <answer> ... <workstep> <title/> ... </workstep> </answer> </worked_example>
                child.tag = 'example'
                newSubChildren = []
                newSubChildren.append(utils.create_node('label', text="Worked example"))
                pos = 1
                for subChild in child:
                    if subChild.tag == 'title':
                        newSubChildren.append(subChild)
                    elif subChild.tag == 'question':
                        newSubChildren.append(subChild)
                        subChild.tag = 'section'
                        subChild.append(utils.create_node('title', text='Question'))
                    elif subChild.tag == 'answer':
                        newSubChildren.append(subChild)
                        subChild.tag = 'section'
                        subChild.append(utils.create_node('title', text='Answer'))
                        for x in subChild:
                            if x.tag == 'workstep':
                                x.tag = 'section'
                childIndex += 1

            elif child.tag == 'note':
                child.insert(0, utils.create_node('label', text={
                    'warning': 'Warning',
                    'tip': 'Tip',
                    'note': 'Note',
                    'aside': 'Interesting Fact'}[child.attrib['type']]))
                childIndex += 1

            elif child.tag == 'math_identity':
                ruleNode = utils.create_node('rule')
                ruleNode.attrib['type'] = 'Identity'
                child.tag = 'statement'
                ruleNode.append(child)
                element[childIndex] = ruleNode
                childIndex += 1

            elif (child.tag == 'number') and (child.getparent().tag != 'entry'):
                if len(child) == 0:
                    # No children, means it's just a plain number
                    coeffText = utils.format_number(child.text.strip())
                    try:
                        dummyNode = etree.fromstring('<dummy>' + coeffText + '</dummy>')
                    except etree.XMLSyntaxError, msg:
                        print repr(coeffText)
                        raise etree.XMLSyntaxError, msg
                else:
                    # Scientific or exponential notation: parse out coefficient, base and exponent
                    coeffNode = child.find('coeff')
                    expNode = child.find('exp')
                    baseNode = child.find('base')
                    if coeffNode is None:
                        # Exponential
                        if baseNode is None:
                            baseText = utils.format_number('10')
                        else:
                            baseText = utils.format_number(baseNode.text.strip())
                        assert expNode is not None, etree.tostring(child)
                        expText = utils.format_number(expNode.text.strip())
                        dummyNode = etree.fromstring('<dummy>' + baseText + '<sup>' + expText + '</sup></dummy>')
                    else:
                        # Scientific notation or plain number (<coeff> only)
                        coeffText = utils.format_number(coeffNode.text.strip())
                        if expNode is None:
                            assert baseNode is None
                            try:
                                dummyNode = etree.fromstring('<dummy>' + coeffText + '</dummy>')
                            except etree.XMLSyntaxError, msg:
                                print repr(coeffText)
                                raise etree.XMLSyntaxError, msg
                        else:
                            if baseNode is None:
                                baseText = utils.format_number('10')
                            else:
                                baseText = utils.format_number(baseNode.text.strip())
                            expText = utils.format_number(expNode.text.strip())
                            dummyNode = etree.fromstring('<dummy>' + coeffText + ' &#215; ' + baseText + '<sup>' + expText + '</sup></dummy>')
                utils.etree_replace_with_node_list(element, child, dummyNode)
                childIndex += len(dummyNode)

            elif child.tag == 'percentage':
                dummyNode = etree.fromstring('<dummy>' + utils.format_number(child.text.strip()) + '%</dummy>')
                utils.etree_replace_with_node_list(element, child, dummyNode)
                childIndex += len(dummyNode)

            elif child.tag == 'unit':
                if child.text is None:
                    child.text = ''
                child.text = child.text.lstrip()
                if len(child) == 0:
                    child.text = child.text.rstrip()
                else:
                    if child[-1].tail is not None:
                        child[-1].tail = child[-1].tail.rstrip()
                if (child.getparent().tag == 'unit_number') and (child.text != u'\xb0'):
                    # Leave space between number and unit, except for degrees
                    child.text = ' ' + child.text
                for sup in child:
                    assert sup.tag == 'sup'
                    sup.text = sup.text.strip().replace('-', u'\u2212')
                utils.etree_replace_with_node_list(element, child, child)
                childIndex += len(child)

            elif child.tag == 'unit_number':
                childIndex += len(child)
                if child.tail not in [None, '']:
                    pass
                utils.etree_replace_with_node_list(element, child, child)

            elif child.tag == 'nuclear_notation':
                namespace = 'http://www.w3.org/1998/Math/MathML'
                mathNode = utils.create_node('math', namespace=namespace)
                mathNode.append(utils.create_node('msubsup', namespace=namespace))
                mathNode[-1].append(utils.create_node('mo', namespace=namespace, text=u'\u200b'))
                mathNode[-1].append(utils.create_node('mn', namespace=namespace, text=child.find('atomic_number').text))
                if child.find('mass_number') is not None:
                    massNumber = child.find('mass_number').text
                else:
                    massNumber = u'\u200b'
                mathNode[-1].append(utils.create_node('mn', namespace=namespace, text=massNumber))
                mathNode.append(utils.create_node('mtext', namespace=namespace, text=child.find('symbol').text))

                mathNode.tail = child.tail
                element[childIndex] = mathNode
                childIndex += 1

            elif child.tag == 'math_extension':
                child.tag = 'note'
                titleNode = child.find('title')
                if titleNode is not None:
                    titleNode.tag = 'label'
                    titleNode.text = u'Extension \u2014 ' + titleNode.text.strip()
                else:
                    child.insert(0, utils.create_node('label', text='Extension'))
                bodyNode = child.find('body')
                utils.etree_replace_with_node_list(child, bodyNode, bodyNode)
                childIndex += 1

            elif child.tag == 'section':
                # Check that it is not an activity section
                if child.getparent().tag != 'activity':
                    shortCodeNode = child.find('shortcode')
                    if shortCodeNode is None:
                        if (child.attrib.get('type') not in ['subsubsection', 'subsubsubsection']) and (child.find('title').text.strip() != 'Chapter summary'):
                            print 'WARNING: no shortcode for section "%s"'%child.find('title').text.strip()
                            shortcode = 'SHORTCODE'
                        else:
                            shortcode = None
                    else:
                        if (child.attrib.get('type') in ['subsubsection', 'subsubsubsection']) or (child.find('title').text.strip() == 'Chapter summary'):
                            print 'WARNING: section "%s" should not have a shortcode'%child.find('title').text.strip()
                        shortcode = shortCodeNode.text.strip()
                        child.remove(shortCodeNode)
                    """ # Commented out so that shortcodes do not get displayed
                    if shortcode is not None:
                        titleNode = child.find('title')
                        if len(titleNode) == 0:
                            if titleNode.text is None:
                                titleNode.text = ''
                            titleNode.text += ' [' + shortcode + ']'
                        else:
                            if titleNode[-1].tail is None:
                                titleNode[-1].tail = ''
                            titleNode[-1].tail += ' [' + shortcode + ']'
                    """
                childIndex += 1

            elif child.tag == 'latex':
                if child.attrib.get('display', 'inline') == 'block':
                    delimiters = '[]'
                else:
                    delimiters = '()'
                if child.text is None:
                    child.text = ''
                child.text = '\\' + delimiters[0] + child.text
                if len(child) > 0:
                    if child[-1].text is None:
                        child[-1].tail = ''
                    child[-1].tail += '\\' + delimiters[1]
                else:
                    child.text += '\\' + delimiters[1]
                utils.etree_replace_with_node_list(element, child, child)
                childIndex += len(child)

            elif child.tag in ['chem_compound', 'spec_note']:
                assert len(child) == 0, "<chem_compound> element not expected to have sub-elements."
                if child.text is None:
                    child.text = ''
                child.text = child.text.strip()
                assert child.text != '', "<chem_compound> element must contain text."

                compoundText = child.text
                pos = 0
                textOpen = False
                while pos < len(compoundText):
                    if 'a' <= compoundText[pos].lower() <= 'z':
                        if not textOpen:
                            compoundText = compoundText[:pos] + r'\text{' + compoundText[pos:]
                            textOpen = True
                            pos += len(r'\text{') + 1
                        else:
                            pos += 1
                    else:
                        if textOpen:
                            compoundText = compoundText[:pos] + '}' + compoundText[pos:]
                            textOpen = False
                            pos += 2
                        else:
                            pos += 1
                if textOpen:
                    compoundText += '}'
                compoundXml = utils.xmlify(r'\(' + compoundText + r'\)')

                compoundDom = etree.fromstring(compoundXml[compoundXml.find('<formula '):compoundXml.rfind('\n</p>')])
                utils.etree_replace_with_node_list(element, child, compoundDom)
                childIndex += len(child)

            else:
                path = [child.tag]
                node = child
                while True:
                    node = node.getparent()
                    if node is None:
                        break
                    path.append(node.tag)
                path.reverse()

                namespaces = {'m': 'http://www.w3.org/1998/Math/MathML'}
                valid = [
                    'emphasis',
                    'para',
                    'figure/type',
                    'exercise/problem', 'exercise/title',
                    'exercise/shortcodes/entry/number', 'exercise/shortcodes/entry/shortcode', 'exercise/shortcodes/entry/url', 'exercise/shortcodes/entry/todo-content',
                    'list/item/label',
                    'table/tgroup/tbody/row/entry',
                    'table/tgroup/colspec',
                    'definition/term', 'definition/meaning',
                    'sup',
                    'sub',
                    'm:mn', 'm:mo', 'm:mi', 'm:msup', 'm:mrow', 'm:math', 'm:mtable', 'm:mtr', 'm:mtd', 'm:msub', 'm:mfrac', 'm:msqrt', 'm:mspace', 'm:mstyle', 'm:mfenced', 'm:mtext', 'm:mroot', 'm:mref', 'm:msubsup', 'm:munderover', 'm:munder', 'm:mover', 'm:mphantom',
                    'equation',
                    'link',
                    'quote',
                    'rule/title', 'rule/statement', 'rule/proof',

                    'section/title',
                    'section/shortcode',
                    'image/arguments',
                    'image/src',
                    'number/coeff', 'number/exp', 'number/base',
                    'nuclear_notation/mass_number', 'nuclear_notation/atomic_number', 'nuclear_notation/symbol',
                    'pspicture/code', 'pspicture/usepackage',
                    'tikzpicture/code',
                    'video/title', 'video/shortcode', 'video/url', 'video/width', 'video/height',
                    'worked_example/answer/workstep/title', 'worked_example/question', 'worked_example/title',
                    'activity/title',
                    'math_extension/title',
                    'math_extension/body',
                    'math_identity',
                    'document/content/title',
                    'document/content/content',
                    'simulation/title', 'simulation/shortcode', 'simulation/url', 'simulation/width', 'simulation/height', 'simulation/embed',
                    'presentation/title', 'presentation/url', 'presentation/shortcode', 'presentation/embed',
                    'box',
                ]
                validSet = set([])
                for entry in valid:
                    entry = entry.split('/')
                    for i in range(len(entry)):
                        if ':' in entry[i]:
                            entry[i] = entry[i].split(':')
                            assert len(entry[i]) == 2
                            entry[i] = '{%s}%s'%(namespaces[entry[i][0]], entry[i][1])
                        validSet.add(tuple(entry[:i+1]))
                valid = validSet

                passed = False
                for entry in valid:
                    if tuple(path[-len(entry):]) == entry:
                        passed = True
                        break
                if not passed:
                    path = '/'.join(path)
                    for key, url in namespaces.iteritems():
                        path = path.replace('{%s}'%url, key+':')
                    LOGGER.info('Unhandled element: ' + path)

                childIndex += 1


def register():
    return cnxmlplus_to_shortcodecnxml()

