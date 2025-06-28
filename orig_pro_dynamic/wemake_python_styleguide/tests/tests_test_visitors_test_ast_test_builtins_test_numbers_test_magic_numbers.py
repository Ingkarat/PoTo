import pytest
from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.constants import MAGIC_NUMBERS_WHITELIST
from wemake_python_styleguide.violations.best_practices import MagicNumberViolation
from wemake_python_styleguide.visitors.ast.builtins import WrongNumberVisitor
assignment = 'constant = {0}'
assignment_typed = 'constant: int = {0}'
assignment_unary = 'constant = -{0}'
walrus = '(constant := {0})'
function_definition = '\ndef function_name(param1, param2={0}):\n    return param1 / param2\n'
function_definition_typed = '\ndef function_name(param1, param2: int = {0}):\n    return param1 / param2\n'
list_definition = '[{0}]'
dict_definition_key = '{{{0}: "value"}}'
dict_definition_value = '{{"first": {0}}}'
set_definition = '{{"first", {0}, "other"}}'
tuple_definition = '({0}, )'
assignment_binop = 'final = {0} + 1'
assignment_binop_typed = 'final: int = {0} + 1'
function_call = 'print({0})'
function_call_named = 'print(end={0})'
expression = '{0}'
inside_function = '\ndef wrapper():\n    some_value = called_func() * {0}\n'
inside_class = '\nclass Test(object):\n    class_field = SOME_CONST - {0}\n'
inside_class_typed = '\nclass Test(object):\n    class_field: int = SOME_CONST - {0}\n'
inside_method = '\nclass Test(object):\n    def method(self):\n        return {0}\n'
list_index = '\nsome_list = [10, 20, 30]\nsome_list[{0}]\n'
dict_key = '\nsome_dict = {{11: 12, 13: 14}}\nsome_dict[{0}]\n'

@pytest.mark.parametrize('code', [assignment, assignment_typed, assignment_unary, pytest.param(walrus, marks=pytest.mark.skipif(not PY38, reason='walrus appeared in 3.8')), function_definition, function_definition_typed, list_definition, dict_definition_key, dict_definition_value, set_definition, tuple_definition])
@pytest.mark.parametrize('number', [-10, -3.5, 0, float(0), 0.1, 0.5, -1.0, 8.3, 10, 765, '0x20', '0o12', '0b1', '1e1', '1j'])
def test_magic_number(assert_errors, parse_ast_tree, code, number, default_options, mode):
    code = assignment
    number = -10
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that there are no magic numbers in this code.'
    tree = parse_ast_tree(mode(code.format(number)))
    visitor = WrongNumberVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [assignment_binop, assignment_binop_typed, function_call, function_call_named, expression, inside_function, inside_class, inside_class_typed, inside_method, list_index, dict_key])
@pytest.mark.parametrize('number', [*MAGIC_NUMBERS_WHITELIST, -0, float(0), 1, 5, 10])
def test_magic_number_whitelist(assert_errors, parse_ast_tree, code, number, default_options, mode):
    code = assignment_binop
    number = *MAGIC_NUMBERS_WHITELIST
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that magic numbers in this code are whitelisted.'
    tree = parse_ast_tree(mode(code.format(number)))
    visitor = WrongNumberVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [assignment_binop, assignment_binop_typed, function_call, function_call_named, expression, inside_function, inside_class, inside_class_typed, inside_method, list_index, dict_key])
@pytest.mark.parametrize('number', ['-0.3', '999', '10.0', '--134', '8.3'])
def test_magic_number_warning(assert_errors, assert_error_text, parse_ast_tree, code, number, default_options, mode):
    code = assignment_binop
    number = '-0.3'
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that magic numbers in this code are warnings.'
    tree = parse_ast_tree(mode(code.format(number)))
    visitor = WrongNumberVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [MagicNumberViolation])
    assert_error_text(visitor, number.replace('-', ''))

@pytest.mark.parametrize('code', [assignment_binop, assignment_binop_typed, function_call, function_call_named, expression, inside_function, inside_class, inside_class_typed, inside_method, list_index, dict_key])
@pytest.mark.parametrize('number', ['0b1111', '0x20', '-0o15'])
def test_magic_number_octal_warning(assert_errors, parse_ast_tree, code, number, default_options, mode):
    code = assignment_binop
    number = '0b1111'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that magic numbers in this code are warnings.'
    tree = parse_ast_tree(mode(code.format(number)))
    visitor = WrongNumberVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [MagicNumberViolation])
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