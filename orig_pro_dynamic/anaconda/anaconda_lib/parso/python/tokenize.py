# -*- coding: utf-8 -*-
"""
This tokenizer has been copied from the ``tokenize.py`` standard library
tokenizer. The reason was simple: The standard library tokenizer fails
if the indentation is not right. To make it possible to do error recovery the
    tokenizer needed to be rewritten.

Basically this is a stripped down version of the standard library module, so
you can read the documentation there. Additionally we included some speed and
memory optimizations here.
"""
from __future__ import absolute_import

import sys
import re
from collections import namedtuple
import itertools as _itertools
from codecs import BOM_UTF8

from parso.python.token import PythonTokenTypes
from parso.utils import split_lines


# Maximum code point of Unicode 6.0: 0x10ffff (1,114,111)
MAX_UNICODE = '\U0010ffff'

STRING = PythonTokenTypes.STRING
NAME = PythonTokenTypes.NAME
NUMBER = PythonTokenTypes.NUMBER
OP = PythonTokenTypes.OP
NEWLINE = PythonTokenTypes.NEWLINE
INDENT = PythonTokenTypes.INDENT
DEDENT = PythonTokenTypes.DEDENT
ENDMARKER = PythonTokenTypes.ENDMARKER
ERRORTOKEN = PythonTokenTypes.ERRORTOKEN
ERROR_DEDENT = PythonTokenTypes.ERROR_DEDENT
FSTRING_START = PythonTokenTypes.FSTRING_START
FSTRING_STRING = PythonTokenTypes.FSTRING_STRING
FSTRING_END = PythonTokenTypes.FSTRING_END

TokenCollection = namedtuple(
    'TokenCollection',
    'pseudo_token single_quoted triple_quoted endpats whitespace '
    'fstring_pattern_map always_break_tokens',
)

BOM_UTF8_STRING = BOM_UTF8.decode('utf-8')

_token_collection_cache = {}

if sys.version_info.major >= 3:
    # Python 3 has str.isidentifier() to check if a char is a valid identifier
    is_identifier = str.isidentifier
else:
    # Python 2 doesn't, but it's not that important anymore and if you tokenize
    # Python 2 code with this, it's still ok. It's just that parsing Python 3
    # code with this function is not 100% correct.
    # This just means that Python 2 code matches a few identifiers too much,
    # but that doesn't really matter.
    def is_identifier(s):
        return True


def group(*choices, **kwargs):
    capture = kwargs.pop('capture', False)  # Python 2, arrghhhhh :(
    assert not kwargs

    start = '('
    if not capture:
        start += '?:'
    return start + '|'.join(choices) + ')'


def maybe(*choices):
    return group(*choices) + '?'


# Return the empty string, plus all of the valid string prefixes.
def _all_string_prefixes(version_info, include_fstring=False, only_fstring=False):
    def different_case_versions(prefix):
        for s in _itertools.product(*[(c, c.upper()) for c in prefix]):
            yield ''.join(s)
    # The valid string prefixes. Only contain the lower case versions,
    #  and don't contain any permuations (include 'fr', but not
    #  'rf'). The various permutations will be generated.
    valid_string_prefixes = ['b', 'r', 'u']
    if version_info.major >= 3:
        valid_string_prefixes.append('br')

    result = set([''])
    if version_info >= (3, 6) and include_fstring:
        f = ['f', 'fr']
        if only_fstring:
            valid_string_prefixes = f
            result = set()
        else:
            valid_string_prefixes += f
    elif only_fstring:
        return set()

    # if we add binary f-strings, add: ['fb', 'fbr']
    for prefix in valid_string_prefixes:
        for t in _itertools.permutations(prefix):
            # create a list with upper and lower versions of each
            #  character
            result.update(different_case_versions(t))
    if version_info.major == 2:
        # In Python 2 the order cannot just be random.
        result.update(different_case_versions('ur'))
        result.update(different_case_versions('br'))
    return result


def _compile(expr):
    return re.compile(expr, re.UNICODE)


def _get_token_collection(version_info):
    try:
        return _token_collection_cache[tuple(version_info)]
    except KeyError:
        _token_collection_cache[tuple(version_info)] = result = \
            _create_token_collection(version_info)
        return result


fstring_string_single_line = _compile(r'(?:\{\{|\}\}|\\(?:\r\n?|\n)|[^{}\r\n])+')
fstring_string_multi_line = _compile(r'(?:[^{}]+|\{\{|\}\})+')
fstring_format_spec_single_line = _compile(r'(?:\\(?:\r\n?|\n)|[^{}\r\n])+')
fstring_format_spec_multi_line = _compile(r'[^{}]+')


def _create_token_collection(version_info):
    # Note: we use unicode matching for names ("\w") but ascii matching for
    # number literals.
    Whitespace = r'[ \f\t]*'
    whitespace = _compile(Whitespace)
    Comment = r'#[^\r\n]*'
    # Python 2 is pretty much not working properly anymore, we just ignore
    # parsing unicode properly, which is fine, I guess.
    if version_info[0] == 2:
        Name = r'([A-Za-z_0-9]+)'
    elif sys.version_info[0] == 2:
        # Unfortunately the regex engine cannot deal with the regex below, so
        # just use this one.
        Name = r'(\w+)'
    else:
        Name = u'([A-Za-z_0-9\u0080-' + MAX_UNICODE + ']+)'

    if version_info >= (3, 6):
        Hexnumber = r'0[xX](?:_?[0-9a-fA-F])+'
        Binnumber = r'0[bB](?:_?[01])+'
        Octnumber = r'0[oO](?:_?[0-7])+'
        Decnumber = r'(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
        Intnumber = group(Hexnumber, Binnumber, Octnumber, Decnumber)
        Exponent = r'[eE][-+]?[0-9](?:_?[0-9])*'
        Pointfloat = group(r'[0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?',
                           r'\.[0-9](?:_?[0-9])*') + maybe(Exponent)
        Expfloat = r'[0-9](?:_?[0-9])*' + Exponent
        Floatnumber = group(Pointfloat, Expfloat)
        Imagnumber = group(r'[0-9](?:_?[0-9])*[jJ]', Floatnumber + r'[jJ]')
    else:
        Hexnumber = r'0[xX][0-9a-fA-F]+'
        Binnumber = r'0[bB][01]+'
        if version_info.major >= 3:
            Octnumber = r'0[oO][0-7]+'
        else:
            Octnumber = '0[oO]?[0-7]+'
        Decnumber = r'(?:0+|[1-9][0-9]*)'
        Intnumber = group(Hexnumber, Binnumber, Octnumber, Decnumber)
        if version_info[0] < 3:
            Intnumber += '[lL]?'
        Exponent = r'[eE][-+]?[0-9]+'
        Pointfloat = group(r'[0-9]+\.[0-9]*', r'\.[0-9]+') + maybe(Exponent)
        Expfloat = r'[0-9]+' + Exponent
        Floatnumber = group(Pointfloat, Expfloat)
        Imagnumber = group(r'[0-9]+[jJ]', Floatnumber + r'[jJ]')
    Number = group(Imagnumber, Floatnumber, Intnumber)

    # Note that since _all_string_prefixes includes the empty string,
    #  StringPrefix can be the empty string (making it optional).
    possible_prefixes = _all_string_prefixes(version_info)
    StringPrefix = group(*possible_prefixes)
    StringPrefixWithF = group(*_all_string_prefixes(version_info, include_fstring=True))
    fstring_prefixes = _all_string_prefixes(version_info, include_fstring=True, only_fstring=True)
    FStringStart = group(*fstring_prefixes)

    # Tail end of ' string.
    Single = r"(?:\\.|[^'\\])*'"
    # Tail end of " string.
    Double = r'(?:\\.|[^"\\])*"'
    # Tail end of ''' string.
    Single3 = r"(?:\\.|'(?!'')|[^'\\])*'''"
    # Tail end of """ string.
    Double3 = r'(?:\\.|"(?!"")|[^"\\])*"""'
    Triple = group(StringPrefixWithF + "'''", StringPrefixWithF + '"""')

    # Because of leftmost-then-longest match semantics, be sure to put the
    # longest operators first (e.g., if = came before ==, == would get
    # recognized as two instances of =).
    Operator = group(r"\*\*=?", r">>=?", r"<<=?",
                     r"//=?", r"->",
                     r"[+\-*/%&@`|^!=<>]=?",
                     r"~")

    Bracket = '[][(){}]'

    special_args = [r'\r\n?', r'\n', r'[;.,@]']
    if version_info >= (3, 0):
        special_args.insert(0, r'\.\.\.')
    if version_info >= (3, 8):
        special_args.insert(0, ":=?")
    else:
        special_args.insert(0, ":")
    Special = group(*special_args)

    Funny = group(Operator, Bracket, Special)

    # First (or only) line of ' or " string.
    ContStr = group(StringPrefix + r"'[^\r\n'\\]*(?:\\.[^\r\n'\\]*)*"
                    + group("'", r'\\(?:\r\n?|\n)'),
                    StringPrefix + r'"[^\r\n"\\]*(?:\\.[^\r\n"\\]*)*'
                    + group('"', r'\\(?:\r\n?|\n)'))
    pseudo_extra_pool = [Comment, Triple]
    all_quotes = '"', "'", '"""', "'''"
    if fstring_prefixes:
        pseudo_extra_pool.append(FStringStart + group(*all_quotes))

    PseudoExtras = group(r'\\(?:\r\n?|\n)|\Z', *pseudo_extra_pool)
    PseudoToken = group(Whitespace, capture=True) + \
        group(PseudoExtras, Number, Funny, ContStr, Name, capture=True)

    # For a given string prefix plus quotes, endpats maps it to a regex
    #  to match the remainder of that string. _prefix can be empty, for
    #  a normal single or triple quoted string (with no prefix).
    endpats = {}
    for _prefix in possible_prefixes:
        endpats[_prefix + "'"] = _compile(Single)
        endpats[_prefix + '"'] = _compile(Double)
        endpats[_prefix + "'''"] = _compile(Single3)
        endpats[_prefix + '"""'] = _compile(Double3)

    # A set of all of the single and triple quoted string prefixes,
    #  including the opening quotes.
    single_quoted = set()
    triple_quoted = set()
    fstring_pattern_map = {}
    for t in possible_prefixes:
        for quote in '"', "'":
            single_quoted.add(t + quote)

        for quote in '"""', "'''":
            triple_quoted.add(t + quote)

    for t in fstring_prefixes:
        for quote in all_quotes:
            fstring_pattern_map[t + quote] = quote

    ALWAYS_BREAK_TOKENS = (';', 'import', 'class', 'def', 'try', 'except',
                           'finally', 'while', 'with', 'return', 'continue',
                           'break', 'del', 'pass', 'global', 'assert')
    if version_info >= (3, 5):
        ALWAYS_BREAK_TOKENS += ('async', 'nonlocal')
    pseudo_token_compiled = _compile(PseudoToken)
    return TokenCollection(
        pseudo_token_compiled, single_quoted, triple_quoted, endpats,
        whitespace, fstring_pattern_map, set(ALWAYS_BREAK_TOKENS)
    )


class Token(namedtuple('Token', ['type', 'string', 'start_pos', 'prefix'])):
    @property
    def end_pos(self):
        lines = split_lines(self.string)
        if len(lines) > 1:
            return self.start_pos[0] + len(lines) - 1, 0
        else:
            return self.start_pos[0], self.start_pos[1] + len(self.string)


class PythonToken(Token):
    def __repr__(self):
        return ('TokenInfo(type=%s, string=%r, start_pos=%r, prefix=%r)' %
                self._replace(type=self.type.name))


class FStringNode(object):
    def __init__(self, quote):
        self.quote = quote
        self.parentheses_count = 0
        self.previous_lines = ''
        self.last_string_start_pos = None
        # In the syntax there can be multiple format_spec's nested:
        # {x:{y:3}}
        self.format_spec_count = 0

    def open_parentheses(self, character):
        self.parentheses_count += 1

    def close_parentheses(self, character):
        self.parentheses_count -= 1
        if self.parentheses_count == 0:
            # No parentheses means that the format spec is also finished.
            self.format_spec_count = 0

    def allow_multiline(self):
        return len(self.quote) == 3

    def is_in_expr(self):
        return self.parentheses_count > self.format_spec_count

    def is_in_format_spec(self):
        return not self.is_in_expr() and self.format_spec_count


def _close_fstring_if_necessary(fstring_stack, string, line_nr, column, additional_prefix):
    for fstring_stack_index, node in enumerate(fstring_stack):
        lstripped_string = string.lstrip()
        len_lstrip = len(string) - len(lstripped_string)
        if lstripped_string.startswith(node.quote):
            token = PythonToken(
                FSTRING_END,
                node.quote,
                (line_nr, column + len_lstrip),
                prefix=additional_prefix+string[:len_lstrip],
            )
            additional_prefix = ''
            assert not node.previous_lines
            del fstring_stack[fstring_stack_index:]
            return token, '', len(node.quote) + len_lstrip
    return None, additional_prefix, 0


def _find_fstring_string(endpats, fstring_stack, line, lnum, pos):
    tos = fstring_stack[-1]
    allow_multiline = tos.allow_multiline()
    if tos.is_in_format_spec():
        if allow_multiline:
            regex = fstring_format_spec_multi_line
        else:
            regex = fstring_format_spec_single_line
    else:
        if allow_multiline:
            regex = fstring_string_multi_line
        else:
            regex = fstring_string_single_line

    match = regex.match(line, pos)
    if match is None:
        return tos.previous_lines, pos

    if not tos.previous_lines:
        tos.last_string_start_pos = (lnum, pos)

    string = match.group(0)
    for fstring_stack_node in fstring_stack:
        end_match = endpats[fstring_stack_node.quote].match(string)
        if end_match is not None:
            string = end_match.group(0)[:-len(fstring_stack_node.quote)]

    new_pos = pos
    new_pos += len(string)
    # even if allow_multiline is False, we still need to check for trailing
    # newlines, because a single-line f-string can contain line continuations
    if string.endswith('\n') or string.endswith('\r'):
        tos.previous_lines += string
        string = ''
    else:
        string = tos.previous_lines + string

    return string, new_pos


def tokenize(code, version_info, start_pos=(1, 0)):
    """Generate tokens from a the source code (string)."""
    lines = split_lines(code, keepends=True)
    return tokenize_lines(lines, version_info, start_pos=start_pos)


def _print_tokens(func):
    """
    A small helper function to help debug the tokenize_lines function.
    """
    def wrapper(*args, **kwargs):
        for token in func(*args, **kwargs):
            print(token)  # This print is intentional for debugging!
            yield token

    return wrapper


# @_print_tokens
def tokenize_lines(lines, version_info, start_pos=(1, 0), indents=None, is_first_token=True):
    """
    A heavily modified Python standard library tokenizer.

    Additionally to the default information, yields also the prefix of each
    token. This idea comes from lib2to3. The prefix contains all information
    that is irrelevant for the parser like newlines in parentheses or comments.
    """
    def dedent_if_necessary(start):
        while start < indents[-1]:
            if start > indents[-2]:
                yield PythonToken(ERROR_DEDENT, '', (lnum, start), '')
                indents[-1] = start
                break
            indents.pop()
            yield PythonToken(DEDENT, '', spos, '')

    pseudo_token, single_quoted, triple_quoted, endpats, whitespace, \
        fstring_pattern_map, always_break_tokens, = \
        _get_token_collection(version_info)
    paren_level = 0  # count parentheses
    if indents is None:
        indents = [0]
    max_ = 0
    numchars = '0123456789'
    contstr = ''
    contline = None
    # We start with a newline. This makes indent at the first position
    # possible. It's not valid Python, but still better than an INDENT in the
    # second line (and not in the first). This makes quite a few things in
    # Jedi's fast parser possible.
    new_line = True
    prefix = ''  # Should never be required, but here for safety
    additional_prefix = ''
    lnum = start_pos[0] - 1
    fstring_stack = []
    for line in lines:  # loop over lines in stream
        lnum += 1
        pos = 0
        max_ = len(line)
        if is_first_token:
            if line.startswith(BOM_UTF8_STRING):
                additional_prefix = BOM_UTF8_STRING
                line = line[1:]
                max_ = len(line)

            # Fake that the part before was already parsed.
            line = '^' * start_pos[1] + line
            pos = start_pos[1]
            max_ += start_pos[1]

            is_first_token = False

        if contstr:                                         # continued string
            endmatch = endprog.match(line)
            if endmatch:
                pos = endmatch.end(0)
                yield PythonToken(
                    STRING, contstr + line[:pos],
                    contstr_start, prefix)
                contstr = ''
                contline = None
            else:
                contstr = contstr + line
                contline = contline + line
                continue

        while pos < max_:
            if fstring_stack:
                tos = fstring_stack[-1]
                if not tos.is_in_expr():
                    string, pos = _find_fstring_string(endpats, fstring_stack, line, lnum, pos)
                    if string:
                        yield PythonToken(
                            FSTRING_STRING, string,
                            tos.last_string_start_pos,
                            # Never has a prefix because it can start anywhere and
                            # include whitespace.
                            prefix=''
                        )
                        tos.previous_lines = ''
                        continue
                    if pos == max_:
                        break

                rest = line[pos:]
                fstring_end_token, additional_prefix, quote_length = _close_fstring_if_necessary(
                    fstring_stack,
                    rest,
                    lnum,
                    pos,
                    additional_prefix,
                )
                pos += quote_length
                if fstring_end_token is not None:
                    yield fstring_end_token
                    continue

            # in an f-string, match until the end of the string
            if fstring_stack:
                string_line = line
                for fstring_stack_node in fstring_stack:
                    quote = fstring_stack_node.quote
                    end_match = endpats[quote].match(line, pos)
                    if end_match is not None:
                        end_match_string = end_match.group(0)
                        if len(end_match_string) - len(quote) + pos < len(string_line):
                            string_line = line[:pos] + end_match_string[:-len(quote)]
                pseudomatch = pseudo_token.match(string_line, pos)
            else:
                pseudomatch = pseudo_token.match(line, pos)

            if pseudomatch:
                prefix = additional_prefix + pseudomatch.group(1)
                additional_prefix = ''
                start, pos = pseudomatch.span(2)
                spos = (lnum, start)
                token = pseudomatch.group(2)
                if token == '':
                    assert prefix
                    additional_prefix = prefix
                    # This means that we have a line with whitespace/comments at
                    # the end, which just results in an endmarker.
                    break
                initial = token[0]
            else:
                match = whitespace.match(line, pos)
                initial = line[match.end()]
                start = match.end()
                spos = (lnum, start)

            if new_line and initial not in '\r\n#' and (initial != '\\' or pseudomatch is None):
                new_line = False
                if paren_level == 0 and not fstring_stack:
                    indent_start = start
                    if indent_start > indents[-1]:
                        yield PythonToken(INDENT, '', spos, '')
                        indents.append(indent_start)
                    for t in dedent_if_necessary(indent_start):
                        yield t

            if not pseudomatch:  # scan for tokens
                match = whitespace.match(line, pos)
                if new_line and paren_level == 0 and not fstring_stack:
                    for t in dedent_if_necessary(match.end()):
                        yield t
                pos = match.end()
                new_line = False
                yield PythonToken(
                    ERRORTOKEN, line[pos], (lnum, pos),
                    additional_prefix + match.group(0)
                )
                additional_prefix = ''
                pos += 1
                continue

            if (initial in numchars                      # ordinary number
                    or (initial == '.' and token != '.' and token != '...')):
                yield PythonToken(NUMBER, token, spos, prefix)
            elif pseudomatch.group(3) is not None:            # ordinary name
                if token in always_break_tokens and (fstring_stack or paren_level):
                    fstring_stack[:] = []
                    paren_level = 0
                    # We only want to dedent if the token is on a new line.
                    m = re.match(r'[ \f\t]*$', line[:start])
                    if m is not None:
                        for t in dedent_if_necessary(m.end()):
                            yield t
                if is_identifier(token):
                    yield PythonToken(NAME, token, spos, prefix)
                else:
                    for t in _split_illegal_unicode_name(token, spos, prefix):
                        yield t  # yield from Python 2
            elif initial in '\r\n':
                if any(not f.allow_multiline() for f in fstring_stack):
                    # Would use fstring_stack.clear, but that's not available
                    # in Python 2.
                    fstring_stack[:] = []

                if not new_line and paren_level == 0 and not fstring_stack:
                    yield PythonToken(NEWLINE, token, spos, prefix)
                else:
                    additional_prefix = prefix + token
                new_line = True
            elif initial == '#':  # Comments
                assert not token.endswith("\n")
                if fstring_stack and fstring_stack[-1].is_in_expr():
                    # `#` is not allowed in f-string expressions
                    yield PythonToken(ERRORTOKEN, initial, spos, prefix)
                    pos = start + 1
                else:
                    additional_prefix = prefix + token
            elif token in triple_quoted:
                endprog = endpats[token]
                endmatch = endprog.match(line, pos)
                if endmatch:                                # all on one line
                    pos = endmatch.end(0)
                    token = line[start:pos]
                    yield PythonToken(STRING, token, spos, prefix)
                else:
                    contstr_start = spos                    # multiple lines
                    contstr = line[start:]
                    contline = line
                    break

            # Check up to the first 3 chars of the token to see if
            #  they're in the single_quoted set. If so, they start
            #  a string.
            # We're using the first 3, because we're looking for
            #  "rb'" (for example) at the start of the token. If
            #  we switch to longer prefixes, this needs to be
            #  adjusted.
            # Note that initial == token[:1].
            # Also note that single quote checking must come after
            #  triple quote checking (above).
            elif initial in single_quoted or \
                    token[:2] in single_quoted or \
                    token[:3] in single_quoted:
                if token[-1] in '\r\n':                       # continued string
                    # This means that a single quoted string ends with a
                    # backslash and is continued.
                    contstr_start = lnum, start
                    endprog = (endpats.get(initial) or endpats.get(token[1])
                               or endpats.get(token[2]))
                    contstr = line[start:]
                    contline = line
                    break
                else:                                       # ordinary string
                    yield PythonToken(STRING, token, spos, prefix)
            elif token in fstring_pattern_map:  # The start of an fstring.
                fstring_stack.append(FStringNode(fstring_pattern_map[token]))
                yield PythonToken(FSTRING_START, token, spos, prefix)
            elif initial == '\\' and line[start:] in ('\\\n', '\\\r\n', '\\\r'):  # continued stmt
                additional_prefix += prefix + line[start:]
                break
            else:
                if token in '([{':
                    if fstring_stack:
                        fstring_stack[-1].open_parentheses(token)
                    else:
                        paren_level += 1
                elif token in ')]}':
                    if fstring_stack:
                        fstring_stack[-1].close_parentheses(token)
                    else:
                        if paren_level:
                            paren_level -= 1
                elif token.startswith(':') and fstring_stack \
                        and fstring_stack[-1].parentheses_count \
                        - fstring_stack[-1].format_spec_count == 1:
                    # `:` and `:=` both count
                    fstring_stack[-1].format_spec_count += 1
                    token = ':'
                    pos = start + 1

                yield PythonToken(OP, token, spos, prefix)

    if contstr:
        yield PythonToken(ERRORTOKEN, contstr, contstr_start, prefix)
        if contstr.endswith('\n') or contstr.endswith('\r'):
            new_line = True

    if fstring_stack:
        tos = fstring_stack[-1]
        if tos.previous_lines:
            yield PythonToken(
                FSTRING_STRING, tos.previous_lines,
                tos.last_string_start_pos,
                # Never has a prefix because it can start anywhere and
                # include whitespace.
                prefix=''
            )

    end_pos = lnum, max_
    # As the last position we just take the maximally possible position. We
    # remove -1 for the last new line.
    for indent in indents[1:]:
        indents.pop()
        yield PythonToken(DEDENT, '', end_pos, '')
    yield PythonToken(ENDMARKER, '', end_pos, additional_prefix)


def _split_illegal_unicode_name(token, start_pos, prefix):
    def create_token():
        return PythonToken(ERRORTOKEN if is_illegal else NAME, found, pos, prefix)

    found = ''
    is_illegal = False
    pos = start_pos
    for i, char in enumerate(token):
        if is_illegal:
            if is_identifier(char):
                yield create_token()
                found = char
                is_illegal = False
                prefix = ''
                pos = start_pos[0], start_pos[1] + i
            else:
                found += char
        else:
            new_found = found + char
            if is_identifier(new_found):
                found = new_found
            else:
                if found:
                    yield create_token()
                    prefix = ''
                    pos = start_pos[0], start_pos[1] + i
                found = char
                is_illegal = True

    if found:
        yield create_token()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        with open(path) as f:
            code = f.read()
    else:
        code = sys.stdin.read()

    from parso.utils import python_bytes_to_unicode, parse_version_string

    if isinstance(code, bytes):
        code = python_bytes_to_unicode(code)

    for token in tokenize(code, parse_version_string()):
        print(token)
