"""
Test to ensure that we count cognitive complexity correctly.

Adapted from https://github.com/Melevir/cognitive_complexity
"""
import pytest
complexity1_1 = '\ndef f(a, b):\n    if a:  # +1\n        return 1\n'
complexity1_2 = '\ndef f(a):\n    return a * f(a - 1)  # +1 for recursion\n'
complexity1_3 = '\nclass Test(object):\n    def f(self, a):\n        return a * self.f(a - 1)  # +1 for recursion\n'
complexity2_1 = '\ndef f(a, b):\n    if a and b and True:  # +2\n        return 1\n'
complexity2_2 = '\ndef f(a, b):\n    if (a):  # +1\n        return 1\n    if b:  # +1\n        return 2\n'
complexity3_1 = '\ndef f(a, b):\n    if a and b or True:  # +3\n        return 1\n'
complexity3_2 = '\ndef f(a, b):\n    if (  # +1\n        a and b and  # +1\n        (c or d)  # +1\n    ):\n        return 1\n'
complexity3_3 = '\ndef f(a, b):\n    if a:  # +1\n        for i in range(b):  # +2\n            return 1\n'
complexity4_1 = '\ndef f(a, b):\n    try:\n        for foo in bar:  # +1\n            return a\n    except Exception:  # +1\n        if a < 0:  # +2\n            return a\n'
complexity4_2 = '\ndef f(a):\n    def foo(a):\n        if a:  # +2\n            return 1\n    bar = lambda a: lambda b: b or 2  # +2\n    return bar(foo(a))(a)\n'
complexity4_3 = "\ndef f(a):\n    if a % 2:  # +1\n        return 'c' if a else 'd'  # +2\n    return 'a' if a else 'b'  # +1\n"
complexity5_1 = '\ndef f(a):\n    valid_items = []\n    for x in a:  # +1\n        if x > 0:  # +2\n            raise ValueError(x)  # +2\n        valid_items.append(x)\n    return valid_items\n'
complexity6_1 = '\ndef f(a, b):\n    if a:  # +1\n        for i in range(b):  # +2\n            if b:  # +3\n                return 1\n'
complexity9_1 = '\ndef f(a):\n    for a in range(10):  # +1\n        if a % 2:  # +2\n            continue  # +2\n        if a == 8:  # +2\n            break  # +2\n'
complexity10_1 = "\ndef process_raw_constant(constant, min_word_length):\n    processed_words = []\n    raw_camelcase_words = []\n    for raw_word in re.findall(r'[a-z]+', constant):  # +1\n        word = raw_word.strip()\n        if (  # +2\n            len(word) >= min_word_length  # +4\n            and not (word.startswith('-') or word.endswith('-'))\n        ):\n            if is_camel_case_word(word):  # +3\n                raw_camelcase_words.append(word)\n            else:\n                processed_words.append(word.lower())\n    return processed_words, raw_camelcase_words\n"
complexity14_1 = "\ndef enhance(tree):\n    for statement in ast.walk(tree):  # +1\n        if not isinstance(statement, ast.If):  # +2\n            continue  # +2\n\n        for child in ast.iter_child_nodes(statement): # +2\n            if isinstance(child, ast.If):  # +3\n                if child in statement.orelse:  # +4\n                    setattr(statement, 'wps_if_chained', True)\n                    setattr(child, 'wps_if_chain', statement)\n    return tree\n"

@pytest.mark.parametrize(('code', 'complexity'), [(complexity1_1, 1), (complexity1_2, 1), (complexity1_3, 1), (complexity2_1, 2), (complexity2_2, 2), (complexity3_1, 3), (complexity3_2, 3), (complexity3_3, 3), (complexity4_1, 4), (complexity4_2, 4), (complexity4_3, 4), (complexity5_1, 5), (complexity6_1, 6), (complexity9_1, 9), (complexity10_1, 10), (complexity14_1, 14)])
def test_cognitive_complexity(get_code_snippet_complexity, mode, code, complexity):
    (code, complexity) = (complexity1_1, 1)
    get_code_snippet_complexity = get_code_snippet_complexity()
    mode = mode()
    'Ensures that cognitive complexity count is correct.'
    assert get_code_snippet_complexity(mode(code)) == complexity
'\nFixtures to make testing cognitive complexity easy.\n\nPolicy for testing cognitive complexity:\n\n1. Use a single function def in code samples\n2. Write ``# +x`` comments on each line where addition happens\n\nAdapted from https://github.com/Melevir/cognitive_complexity\n'
import ast
import pytest
from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.logic.complexity import cognitive

def _find_function(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, FunctionNodes):
            return node
    return None

@pytest.fixture(scope='session')
def get_code_snippet_complexity(parse_ast_tree):
    parse_ast_tree = parse_ast_tree()
    'Fixture to parse and count cognitive complexity the easy way.'

    def factory(src: str) -> int:
        funcdef = _find_function(parse_ast_tree(src))
        assert funcdef, 'No function definition found'
        return cognitive.cognitive_score(funcdef)
    return factory
import ast
import sys
from textwrap import dedent
import pytest
from wemake_python_styleguide.transformations.ast_tree import transform

@pytest.fixture(scope='session')
def parse_ast_tree():
    """
    Function to convert code to AST.

    This helper mimics some transformations that generally
    happen in different ``flake8`` plugins that we rely on.

    This list can be extended only when there's a direct need to
    replicate the existing behavior from other plugin.

    It is better to import and reuse the required transformation.
    But in case it is impossible to do, you can reinvent it.

    Order is important.
    """

    def factory(code: str, do_compile: bool=True) -> ast.AST:
        code_to_parse = dedent(code)
        if do_compile:
            _compile_code(code_to_parse)
        return transform(ast.parse(code_to_parse))
    return factory

def _compile_code(code_to_parse: str) -> None:
    """
    Compiles given string to Python's AST.

    We need to compile to check some syntax features
    that are validated after the ``ast`` is processed:
    like double arguments or ``break`` outside of loops.
    """
    try:
        compile(code_to_parse, '<filename>', 'exec')
    except SyntaxError:
        if sys.version_info[:3] == (3, 9, 0):
            pytest.skip('Python 3.9.0 has strange syntax errors')
        raise
import pytest

@pytest.fixture()
def async_wrapper():
    """Fixture to convert all regular functions into async ones."""

    def factory(template: str) -> str:
        return template.replace('def ', 'async def ').replace('with ', 'async with ').replace('for ', 'async for ')
    return factory

@pytest.fixture()
def regular_wrapper():
    """Fixture to return regular functions without modifications."""

    def factory(template: str) -> str:
        return template
    return factory

@pytest.fixture(params=['async_wrapper', 'regular_wrapper'])
def mode(request):
    """Fixture that returns either `async` or regular functions."""
    return request.getfixturevalue(request.param)