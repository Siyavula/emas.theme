import sys
from lxml import etree
import utils

# Convert CNXML+ down to CNXML
# traverse every element in tree, find matching environments, transform

cnxmlNamespace = "http://cnx.rice.edu/cnxml"
psPictureCount = 0

def traverse_dom_for_cnxml(element):
    global psPictureCount

    for child in element:
        traverse_dom_for_cnxml(child)

    childIndex = 0
    while childIndex < len(element):
        child = element[childIndex]
        if child.tag == 'video':
            #<video><title>...</title><shortcode>...</shortcode>[<url/>]</video>
            mediaNode = utils.create_node('media')
            mediaNode.append(utils.create_node('video'))

            titleNode = child.find('title')
            if titleNode is not None:
                mediaNode.attrib['alt'] = titleNode.text.strip()
            else:
                mediaNode.attrib['alt'] = 'Video'

            urlNode = child.find('url')
            if urlNode is not None:
                mediaNode[0].attrib['src'] = urlNode.text.strip()
            else:
                mediaNode[0].attrib['src'] = ''

            mediaNode.tail = child.tail
            element[childIndex] = mediaNode
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

        elif child.tag == 'pspicture':
            # <pspicture><code>
            #element[childIndex] = child[0]
            psPictureCount += 1
            src = 'pspictures/_%03i.png'%psPictureCount
            mediaNode = utils.create_node('media')
            mediaNode.append(utils.create_node('image'))
            mediaNode.attrib['alt'] = 'Image'
            mediaNode[0].attrib['src'] = src
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

        elif (child.tag == 'number') and (child.getparent().tag != 'entry'):
            coeffNode = child.find('coeff')
            expNode = child.find('exp')
            baseNode = child.find('base')
            if coeffNode is None:
                if baseNode is None:
                    baseText = '10'
                else:
                    baseText = baseNode.text.strip()
                assert expNode is not None, etree.tostring(child)
                expText = expNode.text.strip().replace('-','&#8722;')
                dummyNode = etree.fromstring('<dummy>' + baseText + '<sup>' + expText + '</sup></dummy>')
            else:
                coeffText = coeffNode.text.strip()
                if coeffText[0] in '+-':
                    sign = {'+': '+', '-': '&#8722;'}[coeffText[0]]
                    coeffText = coeffText[1:]
                else:
                    sign = ''
                decimalPos = coeffText.find('.')
                if decimalPos == -1:
                    intPart = coeffText
                    fracPart = None
                else:
                    intPart = coeffText[:decimalPos]
                    fracPart = coeffText[decimalPos+1:]
                # Add thousands separator to integer part
                separator = '&#160;'
                if len(intPart) > 4:
                    pos = len(intPart)-3
                    while pos > 0:
                        intPart = intPart[:pos] + separator + intPart[pos:]
                        pos -= 3
                # Add thousandths separator to fractional part
                if (fracPart is not None) and (len(fracPart) > 4):
                    pos = 3
                    while pos < len(fracPart):
                        fracPart = fracPart[:pos] + separator + fracPart[pos:]
                        pos += 3 + len(separator)
                coeffText = sign + intPart
                if fracPart is not None:
                    coeffText += ',' + fracPart
                if expNode is None:
                    assert baseNode is None
                    dummyNode = etree.fromstring('<dummy>' + coeffText + '</dummy>')
                else:
                    if baseNode is None:
                        baseText = '10'
                    else:
                        baseText = baseNode.text.strip()
                    expText = expNode.text.strip().replace('-','&#8722;')
                    dummyNode = etree.fromstring('<dummy>' + coeffText + ' &#215; ' + baseText + '<sup>' + expText + '</sup></dummy>')
            utils.etree_replace_with_node_list(element, child, dummyNode)
            childIndex += len(dummyNode)

        elif child.tag == 'percentage':
            dummyNode = etree.fromstring('<dummy>' + child.text.strip().replace('.',',').replace('-','&#8722;') + '%</dummy>')
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
            if child.getparent().tag == 'unit_number':
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
            '''
            dummyNode = utils.create_node('dummy')
            dummyNode.append(utils.create_node('sup', text=child.find('mass_number').text))
            dummyNode.append(utils.create_node('sub', text=child.find('atomic_number').text))
            dummyNode[-1].tail = child.find('symbol').text
            utils.etree_replace_with_node_list(element, child, dummyNode)
            childIndex += len(dummyNode)
            '''
            namespace = 'http://www.w3.org/1998/Math/MathML'
            mathNode = utils.create_node('math', namespace=namespace)
            mathNode.append(utils.create_node('msubsup', namespace=namespace))
            mathNode[-1].append(utils.create_node('mo', namespace=namespace, text=u'\u200b'))
            mathNode[-1].append(utils.create_node('mn', namespace=namespace, text=child.find('atomic_number').text))
            mathNode[-1].append(utils.create_node('mn', namespace=namespace, text=child.find('mass_number').text))
            mathNode.append(utils.create_node('mtext', namespace=namespace, text=child.find('symbol').text))

            mathNode.tail = child.tail
            element[childIndex] = mathNode
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
                if shortcode is not None:
                    child.find('title').text += ' [' + shortcode + ']'
            childIndex += 1

        else:
            childIndex += 1

def process(markup):
    # First strip out <section type="chapter">
    dom = etree.fromstring(markup)
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

    traverse_dom_for_cnxml(dom)
    markup = utils.declutter_latex_tags(etree.tostring(dom)).strip()
    assert markup[:8] == '<content'
    assert markup[-10:] == '</content>'
    markup = '<?xml version="1.0"?>\n<document xmlns="http://cnx.rice.edu/cnxml"' + markup[8:-10] + '</document>'

    with open('process_chapter.cnxml','wt') as fp:
        fp.write(markup)


""" Left here just in case someone wants to run the script standalone.
"""
def main():
    """Run the script."""
    if len(sys.argv) < 3:
        print "Usage: cnxmlplus2cnxml [input_file] [output_file]"
        print "Note: Both file names must be fully qualified or relative to this script."
        sys.exit(1)
    
    input_filename = sys.argv[1]
    with open(input_filename, 'rt') as fp:
        markup = fp.read()
        fp.close()
    output_filname = sys.argv[2]
    process(markup, output_filname)

if __name__ == '__main__':
    main()
