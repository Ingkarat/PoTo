import pytest
from wemake_python_styleguide.violations.refactoring import TypeCompareViolation
from wemake_python_styleguide.visitors.ast.functions import WrongFunctionCallContextVisitor
simple_compare = '{0} == other'
is_compare = '{0} is other'
nested_compare = '{0} == int and other()'
triple_compare = '{0} == some == other'
if_case = '\nif {0} == int:\n    ...\n'
expression = '{0}'
assignment = 'some = {0}'
annotation = 'some: {0} = int'
try_finally = '\ntry:\n    file = {0}\nfinally:\n    ...\n'
function_return = '\ndef function():\n    return {0}\n'

@pytest.mark.parametrize('code', [expression, assignment, annotation, try_finally, function_return])
@pytest.mark.parametrize('call', ['type()', 'type(some)', 'type("TypeName", (object,), dict())'])
def test_type_regular_usage(assert_errors, parse_ast_tree, code, call, default_options, mode):
    code = expression
    call = 'type()'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that ``type()`` can be used.'
    tree = parse_ast_tree(mode(code.format(call)))
    visitor = WrongFunctionCallContextVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [simple_compare, is_compare, nested_compare, triple_compare, expression, assignment, annotation, try_finally, function_return])
@pytest.mark.parametrize('call', ['close()', 'type.attr', 'type.attr()', 'obj.type()', 'Type[T]'])
def test_not_type_functions(assert_errors, parse_ast_tree, code, call, default_options, mode):
    code = simple_compare
    call = 'close()'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that regular calls work.'
    tree = parse_ast_tree(mode(code.format(call)))
    visitor = WrongFunctionCallContextVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [simple_compare, is_compare, nested_compare, triple_compare])
@pytest.mark.parametrize('call', ['type()', 'type(some)', 'type("TypeName", (object,), dict())'])
def test_type_with_compare(assert_errors, parse_ast_tree, code, call, default_options, mode):
    code = simple_compare
    call = 'type()'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that ``type()`` cannot be used inside a compare.'
    tree = parse_ast_tree(mode(code.format(call)))
    visitor = WrongFunctionCallContextVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [TypeCompareViolation])
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