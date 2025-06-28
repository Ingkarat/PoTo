import pytest
from wemake_python_styleguide.violations.complexity import TooComplexFormattedStringViolation
from wemake_python_styleguide.violations.consistency import FormattedStringViolation, ModuloStringFormatViolation
from wemake_python_styleguide.visitors.ast.builtins import WrongStringVisitor
_PREFIXES = ('', 'b', 'u', 'r', 'rb', 'f', 'fr')
docstring_module = "'docstring with %s'"
docstring_function = "\ndef test():\n    '''Docstring with %f.'''\n"
docstring_class = "\nclass Test(object):\n    '''Docstring with %d.'''\n"
docstring_method = "\nclass Test(object):\n    def method(self):\n        '''Docstring with %(named)s.'''\n"

@pytest.mark.parametrize('code', ['%10s', '%-10s', '%.5s', '%-10.5s', '%4d', '%06.2f', '%04d', '%+d', '%.*s', '%*.*f', '%%', '%#d', '%0d', '%0*d', '%0*hd', '%0*Li', '%0*li', '%(first)s', '%(f1_abc)+d', '%d-%m-%Y (%H:%M:%S)', '%d', '%i', '%o', '%u', '%x', '%X', '%e', '%E', '%f', '%F', '%g', '%G', '%c', '%r', '%s', '%a'])
@pytest.mark.parametrize('prefix', _PREFIXES)
def test_modulo_formatting(assert_errors, parse_ast_tree, code, prefix, default_options):
    code = '%10s'
    prefix = _PREFIXES[0]
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that the strings violate the rules.'
    tree = parse_ast_tree('x = {0}"{1}"'.format(prefix, code))
    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [ModuloStringFormatViolation], (FormattedStringViolation,))

@pytest.mark.parametrize('code', ['% d', '99.9% of cases', '%10', '10%', '1%0', 'some % name', '%l', '%@', '%.', '%+', '%_%', '\\%\\%', '%\\d', '%[prefix]s', '%(invalid@name)s', '%(also-invalid)d', '', 'regular string', 'some%value', 'some % value', 'some %value', 'some% value', 'to format: {0}', 'named {format}', '%t', '%y', '%m-%Y (%H:%M:%S)'])
@pytest.mark.parametrize('prefix', _PREFIXES)
def test_regular_modulo_string(assert_errors, parse_ast_tree, code, prefix, default_options):
    code = '% d'
    prefix = _PREFIXES[0]
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that the strings violate the rules.'
    tree = parse_ast_tree('x = {0}"{1}"'.format(prefix, code))
    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [], (FormattedStringViolation, TooComplexFormattedStringViolation))

@pytest.mark.parametrize('code', ['dt.strftime("%A, %d. %B %Y %I:%M%p")', 'datetime.strftime("%d-%m-%Y (%H:%M:%S)")', 'datetime.strptime("01-01-2020 (10:20:30)", "%d-%m-%Y (%H:%M:%S)")', 'date.strftime("%d-%m-%Y (%H:%M:%S)")', 'date.strptime("01-01-2020", "%d-%m-%Y")', 'time.strftime("%H:%M:%S")', 'time.strptime("10:20:30", "%H:%M:%S")', 'strptime("01-01-2020 (10:20:30)", "%d-%m-%Y (%H:%M:%S)")', 'cur.execute("SELECT * FROM table WHERE column = %s", ("some_column"))', 'execute("SELECT * FROM table WHERE column = %s", ("some_column"))'])
def test_functions_modulo_string(assert_errors, parse_ast_tree, code, default_options):
    code = 'dt.strftime("%A, %d. %B %Y %I:%M%p")'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that the strings violate the rules.'
    tree = parse_ast_tree(code)
    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [], (FormattedStringViolation,))

@pytest.mark.parametrize('code', ['x % 1', '"str" % 1', 'name % value', '1 % name', '"a" % "b"'])
def test_modulo_operations(assert_errors, parse_ast_tree, code, default_options):
    code = 'x % 1'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that the modulo operations are not affected.'
    tree = parse_ast_tree(code)
    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [docstring_module, docstring_function, docstring_class, docstring_method])
def test_docstring_modulo_operations(assert_errors, parse_ast_tree, code, default_options):
    code = docstring_module
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that the docstrings are allowed.'
    tree = parse_ast_tree(code)
    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])
from typing import Optional, Sequence
import pytest
from wemake_python_styleguide.violations.base import ASTViolation, TokenizeViolation
from wemake_python_styleguide.visitors.base import BaseVisitor

@pytest.fixture(scope='session')
def assert_errors():
    """Helper function to assert visitor violations."""

    def factory(visitor: BaseVisitor, errors: Sequence[str], ignored_types=None):
        if ignored_types:
            real_errors = [error for error in visitor.violations if not isinstance(error, ignored_types)]
        else:
            real_errors = visitor.violations
        assert len(errors) == len(real_errors)
        for (index, error) in enumerate(real_errors):
            assert error.code == errors[index].code
            if isinstance(error, (ASTViolation, TokenizeViolation)):
                assert error._node is not None
                assert error._location() != (0, 0)
    return factory

@pytest.fixture(scope='session')
def assert_error_text():
    """Helper function to assert visitor violation's text."""

    def factory(visitor: BaseVisitor, text: str, baseline: Optional[int]=None, *, multiple: bool=False):
        if not multiple:
            assert len(visitor.violations) == 1
        violation = visitor.violations[0]
        error_format = ': {0}'
        assert error_format in violation.error_template
        assert violation.error_template.endswith(error_format)
        reproduction = violation.__class__(node=violation._node, text=text, baseline=baseline)
        assert reproduction.message() == violation.message()
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