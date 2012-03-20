import asciimathml
from logging import getLogger

LOGGER = getLogger('%s:' % __name__)

# These non-LaTeX commands do not exist in the ASCIIMathML spec, but
# are somehow rendered on FullMarks
bogusAsciimathmlCommands = {
    'cdot': '*',
}

# LaTeX commands with ASCIIMathML equivalents
latexSubstitutions = {
    r'\approx': '~~',
    r'\backslash': r'\\',
    r'\bigcap': 'nnn',
    r'\bigcup': 'uuu',
    r'\bigvee': 'vvv',
    r'\bigwedge': '^^^',
    r'\bot': '_|_',
    r'\cap': 'nn',
    r'\circ': '@',
    r'\cong': '~=',
    r'\cup': 'uu',
    r'\divide': '-:',
    r'\downarrow': 'darr',
    r'\emptyset': 'O/',
    r'\equiv': '-=',
    r'\exists': 'EE',
    r'\forall': 'AA',
    r'\ge': '>=',
    r'\geq': '>=',
    r'\implies': '=>',
    r'\infty': 'oo',
    r'\langle': '(:',
    r'\lceiling': '|~',
    r'\ldots': '...',
    r'\le': '<=',
    r'\Leftarrow': 'lArr',
    r'\leftarrow': 'larr',
    r'\Leftrightarrow': 'hArr',
    r'\leftrightarrow': 'harr',
    r'\leq': '<=',
    r'\lfloor': '|__',
    r'\mathbb': 'bbb',
    r'\mathbf': 'bb',
    r'\mathcal': 'cc',
    r'\mathfrak': 'fr',
    r'\mathsf': 'sf',
    r'\mathtt': 'tt',
    r'\models': '|=',
    r'\nabla': 'grad',
    r'\ne': '!=',
    r'\neg': 'not',
    r'\notin': '!in',
    r'\oplus': 'o+',
    r'\otimes': 'ox',
    r'\partial': 'del',
    r'\pm': '+-',
    r'\prec': '-<',
    r'\propto': 'prop',
    r'\rangle': ':)',
    r'\rceiling': '~|',
    r'\rfloor': '__|',
    r'\Rightarrow': 'rArr',
    r'\rightarrow': 'rarr',
    r'\subset': 'sub',
    r'\subseteq': 'sube',
    r'\succ': '>-',
    r'\supset': 'sup',
    r'\supseteq': 'supe',
    r'\therefore': ':.',
    r'\times': 'xx',
    r'\to': 'rarr',
    r'\top': 'TT',
    r'\uparrow': 'uarr',
    r'\vdash': '|-',
    r'\vee': 'vv',
    r'\wedge': '^^',
}

# Wrapper around asciimathml.parse function, to handle issues with
# parse ASCIIMathML content from FullMarks
__asciimathml_parse_original__ = asciimathml.parse
def __asciimathml_parse_modified__(s, *args, **kwargs):
    # Replace "..." with text{...}
    if s.count('"') % 2 == 0:
        stop = 0
        while True:
            start = s.find('"', stop)
            if start == -1:
                break
            stop = s.find('"', start+1)
            s = s[:start] + ' text{' + s[start+1:stop] + '}' + s[stop+1:]
            stop += 4
    else:
        LOGGER.info('ERROR: ASCIIMathML wrapper refused to remove quotes since there were an odd number of them.')
    # Replace \command with LaTeX mapping, or with command if no
    # mapping (exceptions: r"\\" and r"\ ")
    pos = 0
    while True:
        pos = s.find('\\', pos)
        if pos == -1:
            break
        if pos == len(s)-1:
            LOGGER.info('ERROR: Backslash at end of ASCIIMathML string.')
            break
        if s[pos+1] in ['\\', ' ']:
            pos += 2
        elif s[pos+1].isalpha():
            # Parse command, map it through LaTeX command list
            start = pos
            pos += 2
            while (pos < len(s)) and s[pos].isalpha():
                pos += 1
            command = s[start:pos]
            command = ' ' + latexSubstitutions.get(command, command[1:]) + ' '
            s = s[:start] + command + s[pos:]
            pos = start + len(command)
        else:
            # Assume that the backslash is meant to be there
            pos += 1
    # Replace bogus ASCIIMathML commands
    for command in bogusAsciimathmlCommands:
        start = 0
        while True:
            start = s.find(command, start)
            if start == -1:
                break
            stop = start + len(command)
            if ((start == 0) or (s[start-1].lower() < 'a') or (s[start-1].lower() > 'z')) and ((stop == len(s)) or (s[stop].lower() < 'a') or (s[stop].lower() > 'z')):
                replacement = ' ' + bogusAsciimathmlCommands[command] + ' '
                s = s[:start] + replacement + s[stop:]
                start += len(replacement)
            else:
                start = stop
    # Pass string to asciimathml.parse
    return __asciimathml_parse_original__(s, *args, **kwargs)
asciimathml.parse = __asciimathml_parse_modified__
