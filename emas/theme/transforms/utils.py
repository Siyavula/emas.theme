def fix_newlines(latex):
    return latex.replace('\r\n', '\n')


def strip_comments(latex):
    # Strip out everything from a % to a newline
    start = 0
    newLatex = ''
    while True:
        stop = latex.find('%', start)
        if stop == -1:
            newLatex += latex[start:]
            break
        if (stop > 0) and (latex[stop-1] == '\\'):
            newLatex += latex[start:stop+1]
            start = stop+1
        else:
            newLatex += latex[start:stop]
            endOfLine = latex.find('\n', stop)
            if endOfLine == -1:
                break
            start = endOfLine+1
    return newLatex


def normalize_spacing(latex):
    # Replace \par with newlines.
    commandChar = 'abcdefghijklmnopqrstuvwxyz*'
    pos = 0
    while True:
        pos = latex.find('\\par', pos)
        if pos == -1:
            break
        if latex[pos+4].lower() not in commandChar:
            latex = latex[:pos] + '\n\n' + latex[pos+4:]
        else:
            pos += 4
    # Collapse multiple newlines.
    pos = 0
    while True:
        start = latex.find('\n', pos)
        if start == -1:
            break
        stop, newLines = skip_whitespace(latex, start+1, countNewLines=True)
        if newLines > 0:
            latex = latex[:start] + '\n\n' + latex[stop:]
            pos = start+2
        else:
            pos = stop
    # Strip spaces out of environment names
    pos = 0
    while True:
        pos, command = get_next_command(latex, start=pos, command=['\\begin', '\\end'])
        if pos == -1:
            break
        pos += len(command)
        argument = parse_argument(latex, delimiter='{}', start=pos)
        environment = argument.strip()[1:-1].strip()
        if len(environment)+2 < len(argument):
            latex = latex[:pos] + '{' + environment + '}' + latex[pos+len(argument):]
        
    return latex


def skip_whitespace(latex, start=0, countNewLines=False):
    newLines = 0
    while (start < len(latex)) and (latex[start] in '\r\n\t '):
        if latex[start] == '\n':
            newLines += 1
        start += 1
    if countNewLines:
        return start, newLines
    else:
        return start


def parse_argument(latex, delimiter='{}', start=0):
    pos = skip_whitespace(latex, start)
    if (pos >= len(latex)) or (latex[pos] != delimiter[0]):
        raise ValueError, "Expected %s. Context: %s."%(repr(delimiter[0]), repr(latex[start:pos+20]))
    pos += 1
    delimiterCount = 1
    while delimiterCount > 0:
        if pos >= len(latex):
            raise ValueError, "Reached end of string before finishing argument."
        if latex[pos] == '\\':
            pos += 1 # skip next character since it is escaped
        elif latex[pos] == delimiter[0]:
            delimiterCount += 1
        elif latex[pos] == delimiter[1]:
            delimiterCount -= 1
        pos += 1
    return latex[start:pos]


def get_next_command(latex, start=None, stop=None, command=None):
    """
    Arguments:

      latex -- The LaTeX string in which to search.
      start -- The index from which to start searching.
      stop -- The last index at which a command can start.
      command -- Can be a string, a list of strings or None. If it is
        a string, it represents the command (starting with a
        backslash) to search for. If it is a list of strings, it
        specifies a set of commands to search for. If None, the first
        LaTeX command found will be returned.

    Returns:

      If command is None or a list of strings: return (index,
        command), the index in the string of the start of the command
        (the backslash) and the command.

      If command is a string: return only the index at which the
      command was found.

      If a command was not found, the returned index will be -1 and
      the returned command (if it gets returned) will be None.
    """
    index = start
    while True:
        index = latex.find('\\', index, stop)
        if index == -1:
            if isinstance(command, basestring):
                return -1
            else:
                return -1, None # (index, command)
        pos = index+1
        while pos < len(latex):
            if 'a' <= latex[pos].lower() <= 'z':
                pos += 1
                continue
            if latex[pos] == '*':
                pos += 1
                break
            break
        foundCommand = latex[index:pos]
        if command is None:
            return index, foundCommand
        elif isinstance(command, basestring):
            if foundCommand == command:
                return index
        elif foundCommand in command: # Assume that command is a list / tuple / set / ...
            return index, foundCommand
        index = pos


def get_next_environment(latex, start=None, stop=None, environment=None, returnLatex=True, closing=False):
    """
    Arguments:

      latex -- The LaTeX string in which to search.
      start -- The index from which to start searching.
      stop -- The last index at which a command can start.
      environment -- Can be a string, a list of strings or None. If it
        is a string, it represents the environment name to search
        for. If it is a list of strings, it specifies a set of
        environments to search for. If None, the first LaTeX
        environment found will be returned.
      returnLatex -- Whether to return the full LaTeX of the opening
        environment command (\begin{...}).

    Returns:

      If environment is None or a list of strings: return (index,
      environment), the index in the string of the start of the
      environment (\begin{...}) and the environment name.

      If environment is a string: return only the index at which the
      environment was found.

      If an environment was not found, the returned index will be -1 and
      the returned environment name (if it gets returned) will be None.

      If returnLatex is True, the LaTeX command that opens the
        environment, \begin{...}, including all whitespace will also
        be returned.
    """
    index = start
    if closing:
        searchCommand = '\\end'
    else:
        searchCommand = '\\begin'
    while True:
        index = get_next_command(latex, start=index, stop=stop, command=searchCommand)
        if index == -1:
            result = [-1]
            if isinstance(environment, basestring):
                pass
            else:
                result.append(None)
            if returnLatex:
                result.append('')
            return tuple(result)
        argument = parse_argument(latex, start=index+len(searchCommand))
        foundEnvironment = argument.strip()[1:-1].strip()
        result = [index]
        if environment is None:
            result.append(foundEnvironment)
        elif isinstance(environment, basestring):
            if foundEnvironment == environment:
                pass
            else:
                result = None
        elif foundEnvironment in environment: # Assume that environment is a list / tuple / set / ...
            result.append(foundEnvironment)
        else:
            result = None
        if result is not None:
            if returnLatex:
                result.append(latex[index:index+len(searchCommand)+len(argument)])
            return tuple(result)
        index += len(searchCommand) + len(argument)


def find_all_environments(latex, start=None, exclude=[]):
    start = 0
    environmentStack = []
    result = []
    while True:
        pos, command = get_next_command(latex, start=start, command=[r'\begin',r'\end'])
        if command == r'\begin':
            start = pos + len(command)
            argument = parse_argument(latex, start=start)
            environment = argument.strip()[1:-1].strip()
            if environment not in exclude:
                environmentStack.append([pos, None, environment]) # [start, stop, environment name]
            start += len(argument)
        elif command == r'\end':
            start = pos + len(command)
            argument = parse_argument(latex, start=start)
            environment = argument.strip()[1:-1].strip()
            start += len(argument)
            if environment not in exclude:
                if environment != environmentStack[-1][2]:
                    print '-------------------------------'
                    print latex
                    print '-------------------------------'
                    raise ValueError, "Unmatched environment commands \\begin{%s} and \\end{%s}."%(environmentStack[-1][2], environment)
                environmentStack[-1][1] = start
                result.append(environmentStack.pop())
        else: # command is None:
            if len(environmentStack) != 0:
                print '-------------------------------'
                print latex
                print '-------------------------------'
                raise ValueError, "Environment stack not empty: " + repr(environmentStack)
            break
    return result


ignoreCommands = {
    '\\addcontentsline': 3,
    '\\addtocounter': 2,
    '\\fancyfoot': 1,
    '\\newpage': 0,
    '\\clearpage': 0,
    '\\noindent': 0,
    '\\nopagebreak': 0,
    '\\pagebreak': 0,
    '\\setcounter': 2,
    '\\vspace': 1,
    '\\vspace*': 1,
    '\\rule': 2,
}

def strip_ignore(latex):
    global ignoreCommands
    
    pos = 0
    while True:
        start, command = get_next_command(latex, start=pos, command=ignoreCommands.keys())
        if start == -1:
            break
        stop = start + len(command)
        argumentCount = ignoreCommands[command]
        if argumentCount > 0:
            stop = skip_whitespace(latex, start=stop)
            if latex[stop] == '[':
                # Skip optional arguments
                stop += len(parse_argument(latex, delimiter='[]', start=stop))
            for i in range(argumentCount):
                stop += len(parse_argument(latex, delimiter='{}', start=stop))
        latex = latex[:start] + latex[stop:]
        pos = start
        
    return latex


preambleCommands = {
    r'\ms': r'$\text{m}\cdot\text{s}^{-1}$',
    r'\ohm': r'\ensuremath{\Omega}',
    r'\eohm': r'\,\Omega',
    r'\eN': r'\,\rm{N}',
    r'\emm': r'\,\rm{m}',
    r'\ep': r'\,\ekg \cdot \mbox{\ms}',
    r'\es': r'\,\text{s}',
    r'\ekg': r'\,\text{kg}',
    r'\eJ': r'\,\text{J}',
    r'\eA': r'\,\text{A}',
    r'\eV': r'\,\text{V}',
    r'\eW': r'\,\text{W}',
    r'\ms': r'$\text{m}\cdot\text{s}^{-1}$',
    r'\mss': r'$\text{m}\cdot\text{s}^{-2}$',
    r'\ems': r'\,\text{m} \cdot \text{s}^{-1}',
    r'\emss': r'\,\text{m} \cdot \text{s}^{-2}',
    r'\px': r'$x$',
    r'\py': r'$y$',
    r'\edx': r'\Delta x',
    r'\dx': r'$\edx$',
    r'\edy': r'\Delta y',
    r'\dy': r'$\edy$',
    r'\edt': r'\Delta t',
    r'\dt': r'$\edt$',
    r'\vel': r'$v$',
    r'\kph': r'km$\cdot$hr$^{-1}$',
    r'\momen': r'\vec{p}',
    r'\kener': r'KE',
    r'\poten': r'PE',
    r'\degree': r'^{\circ}',
    r'\ie': r'{\em i.e.~}',
    r'\eg': r'{\em e.g.~}',
    r'\cf': r'{\em c.f.~}',
    r'\resp': r'{\em resp.~}',
    r'\etc': r'{\em etc.~}',
    r'\nb': r'{\em n.b.~}',
    r'\eJSI': r'{\,\text{kg} \cdot \text{m}^{2} \cdot \text{s}^{-2}}',
    r'\ud': r'\mathrm{d}',
}

def parse_preamble(latex):
    global preambleCommands
    
    pos = 0
    while True:
        # Find next LaTeX command
        start, command = get_next_command(latex, start=pos, command=preambleCommands.keys())
        if start == -1:
            break
        pos = start + len(command)

        # Check whether it is from the preamble
        pattern = preambleCommands.get(command)
        if pattern is None:
            continue

        # Read arguments
        arguments = []
        for i in range(pattern.count('%') - 2*pattern.count('%%')):
            argument = parse_argument(latex, start=pos)
            arguments.append(argument.strip()[1:-1])
            pos += len(argument)

        # Modify LaTeX
        latex = latex[:start] + pattern%tuple(arguments) + latex[pos:]
        pos = start
        
    return latex


def traverse_dom_for_tag(dom, tag, callback):
    # dom gets edited in place
    domText = dom.text
    domTail = dom.tail
    domAttrib = dict(dom.attrib)
    domChildren = dom.getchildren()
    dom.clear()
    dom.text = domText
    dom.tail = domTail
    dom.attrib.update(domAttrib)
    #domPos = 0
    #while domPos < len(dom):
    for child in domChildren:
        #child = dom[domPos]
        if child.tag == tag:
            newNodes = callback(child)
            if newNodes is not None:
                #del dom[domPos]
                #for j in range(len(newNodes)-1, -1, -1):
                #    dom.insert(domPos, newNodes[j])
                #domPos += len(newNodes)
                for node in newNodes:
                    dom.append(node)
            else:
                # Unchanged
                #domPos += 1
                dom.append(child)
        else:
            traverse_dom_for_tag(child, tag, callback)
            #domPos += 1
            dom.append(child)

def traverse_dom_for_latex(dom, callback):
    # dom gets edited in place
    domPos = 0
    while domPos < len(dom):
        if dom[domPos].tag == 'latex':
            oldLatex = dom[domPos].text
            newNodes = callback(dom[domPos])
            del dom[domPos]
            if len(newNodes) > 0:
                for j in range(len(newNodes)-1, -1, -1):
                    dom.insert(domPos, newNodes[j])
                if (dom[domPos].tag == 'latex') and (dom[domPos].text == oldLatex):
                    domPos += 1
        else:
            traverse_dom_for_latex(dom[domPos], callback)
            domPos += 1


def declutter_latex_tags(markup):
    substrStart = "<latex>"
    substrStop = "</latex>"
    pos = 0
    newMarkup = ''
    while True:
        start = markup.find(substrStart, pos)
        if start == -1:
            newMarkup += markup[pos:]
            break
        stop = markup.find(substrStop, start)
        if markup[start+len(substrStart):stop].strip() == '':
            newMarkup += markup[pos:start]
            pos = stop + len(substrStop)
        else:
            stop += len(substrStop)
            newMarkup += markup[pos:stop]
            pos = stop
    return newMarkup


def create_node(tag, text=None, namespace=None):
    from lxml import etree
    try:
        if namespace is None:
            node = etree.fromstring('<' + tag + '></' + tag + '>')
        else:
            node = etree.fromstring('<' + tag + ' xmlns="%s"></'%namespace + tag + '>')
    except etree.XMLSyntaxError, msg:
        print tag, namespace
        raise etree.XMLSyntaxError, msg
    if text is not None:
        node.text = text
    return node


def match_dom_pattern(instance, template, varDict={}):
    if instance.tag != template.tag:
        return False
    for key in template.attrib.keys():
        if (key[:2] == '__') and (key[-2:] == '__'):
            continue
        if instance.attrib.get(key) != template.attrib[key]:
            return False
    if (template.text is not None) and (template.text.strip() != ''):
        templateText = template.text.strip()
        if (templateText[:2] == '__') and (templateText[-2:] == '__'):
            varKey = templateText[2:-2]
            varDict[varKey] = instance.text
        elif (instance.text is None) or (instance.text.strip() != templateText):
            return False

    # Recurse through children, skipping optional elements where appropriate
    instanceIndex = 0
    templateIndex = 0
    while instanceIndex < len(instance):
        if templateIndex >= len(template):
            return False
        if match_dom_pattern(instance[instanceIndex],
                             template[templateIndex], varDict):
            instanceIndex += 1
            templateIndex += 1
        else:
            if not eval(template[templateIndex].attrib.get('__optional__', 'False')):
                return False
            templateIndex += 1
    while templateIndex < len(template):
        if not eval(template[templateIndex].attrib.get('__optional__', 'False')):
            return False
        templateIndex += 1
    return True


def etree_replace_with_node_list(parent, child, dummyNode, keepTail=True):
    index = parent.index(child)
    if keepTail and (child.tail is not None):
        childTail = child.tail
    else:
        childTail = ''
    del parent[index]

    if dummyNode.text is not None:
        if index == 0:
            if parent.text is None:
                parent.text = dummyNode.text
            else:
                parent.text += dummyNode.text
        else:
            if parent[index-1].tail is None:
                parent[index-1].tail = dummyNode.text
            else:
                parent[index-1].tail += dummyNode.text

    if len(dummyNode) == 0:
        if index == 0:
            if parent.text is None:
                parent.text = childTail
            else:
                parent.text += childTail
        else:
            if parent[index-1].tail is None:
                parent[index-1].tail = childTail
            else:
                parent[index-1].tail += childTail
    else:
        if dummyNode[-1].tail is None:
            dummyNode[-1].tail = childTail
        else:
            dummyNode[-1].tail += childTail
        for i in range(len(dummyNode)-1, -1, -1):
            parent.insert(index, dummyNode[i])


def base26decode(base26number):
    result = 0
    for digit in base26number:
        result *= 26
        result += ord(digit.lower()) - ord('a') + 1
    return result


def base26encode(integer):
    result = ''
    while integer > 0:
        integer -= 1
        result = chr(integer % 26  + ord('A')) + result
        integer //= 26
    return result


from html_entities import mapping as html_entity_mapping
def xmlify(latex, singleElement=False):
    import tempfile, subprocess, os, shutil
    global html_entity_mapping

    # Remove trailing newlines and other crud
    latex = latex.strip()
    stripTrailing = ['{}', r'\\', r'\newline']
    done = False
    while not done:
        done = True
        for s in stripTrailing:
            if latex[-len(s):] == s:
                latex = latex[:-len(s)].strip()
                done = False
                break
    if latex == '':
        return ''

    tempDir = tempfile.mkdtemp()
    latexPath = os.path.join(tempDir, 'temp.tex')
    xmlPath = os.path.join(tempDir, 'temp.xml')

    # Write LaTeX
    with open(latexPath, 'wt') as fp:
        fp.write(latex.encode('utf-8'))

    # Run tralics
    proc = subprocess.Popen(["tralics", latexPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait()

    # Read back XML and clean up
    with open(xmlPath, 'rt') as fp:
        xml = fp.read().decode('latin-1')
    shutil.rmtree(tempDir)
    substr = '<unknown>'
    start = xml.find(substr)
    assert start != -1
    start += len(substr)
    stop = xml.rfind("</unknown>")
    xml = xml[start:stop].strip()

    if singleElement:
        assert xml[:3] == '<p>'
        assert xml[-4:] == '</p>'
        xml = xml[3:-4].strip()

    pos = 0
    while True:
        start = xml.find('&', pos)
        if start == -1:
            break
        stop = xml.find(';', start)
        assert stop != -1
        stop += 1
        entity = xml[start:stop]
        entity = html_entity_mapping.get(entity, entity)
        xml = xml[:start] + entity + xml[stop:]
        pos = start + len(entity)

    return xml

def format_number(numString, decimalSeparator=',', thousandsSeparator='&#160;'):
    """
    Replace standard decimal point with new decimal separator
    (default: comma); add thousands and thousandths separators
    (default: non-breaking space).
    """
    if numString[0] in '+-':
        sign = {'+': '+', '-': '&#8722;'}[numString[0]]
        numString = numString[1:]
    else:
        sign = ''
    decimalPos = numString.find('.')
    if decimalPos == -1:
        intPart = numString
        fracPart = None
    else:
        intPart = numString[:decimalPos]
        fracPart = numString[decimalPos+1:]
    # Add thousands separator to integer part
    if len(intPart) > 4:
        pos = len(intPart)-3
        while pos > 0:
            intPart = intPart[:pos] + thousandsSeparator + intPart[pos:]
            pos -= 3
    # Add thousandths separator to fractional part
    if (fracPart is not None) and (len(fracPart) > 4):
        pos = 3
        while pos < len(fracPart):
            fracPart = fracPart[:pos] + thousandsSeparator + fracPart[pos:]
            pos += 3 + len(thousandsSeparator)
    numString = sign + intPart
    if fracPart is not None:
        numString += decimalSeparator + fracPart
    return numString
