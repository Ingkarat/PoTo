"""
Integration test that our linter does not break on different random programs.

We generate thousands of them with the help of ``hypothesis`` and ensure
that they are parsed and processed correctly.

We cannot tell whether or not violations are correctly shown by a random input,
but we can tell that our program did not raise any exceptions at least.

See also:
    https://github.com/HypothesisWorks/hypothesis
    https://github.com/Zac-HD/hypothesmith

"""
import io
import tokenize
import hypothesmith
from hypothesis import HealthCheck, given, reject, settings
from wemake_python_styleguide.checker import Checker
settings.register_profile('slow', deadline=None, suppress_health_check=HealthCheck.all())
settings.load_profile('slow')

def _fixup(string: str) -> str:
    """Avoid known issues with tokenize() by editing the string."""
    return ''.join((char for char in string if char.isprintable())).strip().strip('\\').strip() + '\n'

@given(source_code=hypothesmith.from_grammar().map(_fixup))
@settings(print_blob=True)
def test_no_exceptions(source_code, default_options, parse_ast_tree, parse_tokens):
    default_options = default_options()
    parse_ast_tree = parse_ast_tree()
    parse_tokens = parse_tokens()
    '\n    This testcase is a complex example of magic.\n\n    We use property based-test to generate python programs for us.\n    And then we ensure that our linter does not crash on arbitrary input.\n    '
    try:
        tree = parse_ast_tree(str(source_code.encode('utf-8-sig')))
    except (UnicodeEncodeError, SyntaxError):
        reject()
        raise
    lines = io.StringIO(source_code)
    tokens = list(tokenize.generate_tokens(lambda : next(lines)))
    Checker.parse_options(default_options)
    checker = Checker(tree, tokens)
    for violation in checker.run():
        assert isinstance(violation[0], int)
        assert isinstance(violation[1], int)
        assert violation[2].startswith('WPS'), violation[2]
        assert 'WPS0' not in violation[2]
        assert violation[3] == Checker
import os
from collections import namedtuple
import pytest
from wemake_python_styleguide.options.config import Configuration
pytest_plugins = ['plugins.violations', 'plugins.ast_tree', 'plugins.tokenize_parser', 'plugins.async_sync']

@pytest.fixture(scope='session')
def absolute_path():
    """Fixture to create full path relative to `contest.py` inside tests."""

    def factory(*files: str):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, *files)
    return factory

@pytest.fixture(scope='session')
def options():
    """Returns the options builder."""
    default_values = {option.long_option_name[2:].replace('-', '_'): option.default for option in Configuration._options}
    Options = namedtuple('options', default_values.keys())

    def factory(**kwargs):
        final_options = default_values.copy()
        final_options.update(kwargs)
        return Options(**final_options)
    return factory

@pytest.fixture(scope='session')
def default_options(options):
    """Returns the default options."""
    return options()
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
import io
import tokenize
from textwrap import dedent
import pytest

@pytest.fixture(scope='session')
def parse_tokens():
    """Parses tokens from a string."""

    def factory(code: str):
        lines = io.StringIO(dedent(code))
        return list(tokenize.generate_tokens(lambda : next(lines)))
    return factory

@pytest.fixture(scope='session')
def parse_file_tokens(parse_tokens):
    """Parses tokens from a file."""

    def factory(filename: str):
        with open(filename, 'r', encoding='utf-8') as test_file:
            file_content = test_file.read()
            return parse_tokens(file_content)
    return factory