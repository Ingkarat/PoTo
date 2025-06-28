import pytest
from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.violations.complexity import TooManyLocalsViolation
from wemake_python_styleguide.visitors.ast.complexity.function import FunctionComplexityVisitor
function_with_locals = '\ndef function():\n    local_variable1 = 1\n    local_variable2 = 2\n    _ = None  # `_` is not counted\n'
function_with_walrus = '\ndef function():\n    (local_variable1 := 1)\n    (local_variable2 := 2)\n    (_ := None)  # `_` is not counted\n'
function_with_locals_redefinition = '\ndef function():\n    local_variable1 = 1\n    local_variable2 = 2\n\n    local_variable1 += 3\n    local_variable2 = local_variable1 + 4\n'
function_with_locals_and_params = '\ndef function(param):\n    local_variable1 = 1\n    param = param + 2\n    param += 3\n'
function_with_comprehension = '\ndef function():\n    variable1 = [node for node in parse()]\n    variable2 = [xml for xml in variable1]\n'
function_with_nested = '\ndef function():  # has two local vars\n    def factory():  # has one local var\n        variable1 = 1\n\n    variable2 = 2\n'
function_with_nested_and_params = '\ndef function(param1):  # has two local vars\n    param1 = param1 + 1\n\n    def factory(param2):  # has one local var\n        param2 = param2 + 2\n'
method_with_locals = '\nclass Some(object):\n    def function():\n        local_variable1 = 1\n        local_variable2 = 2\n'

@pytest.mark.parametrize('code', [function_with_locals, pytest.param(function_with_walrus, marks=pytest.mark.skipif(not PY38, reason='walrus appeared in 3.8')), function_with_locals_redefinition, function_with_locals_and_params, function_with_comprehension, function_with_nested, function_with_nested_and_params, method_with_locals])
def test_locals_correct_count(assert_errors, parse_ast_tree, options, code, mode):
    code = function_with_locals
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    options = options()
    mode = mode()
    '\n    Testing that local variables are counted correctly.\n\n    Regression test for #74.\n    See: https://github.com/wemake-services/wemake-python-styleguide/issues/74\n\n    Regression test for #247\n    See: https://github.com/wemake-services/wemake-python-styleguide/issues/247\n    '
    option_values = options(max_local_variables=2)
    tree = parse_ast_tree(mode(code))
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [function_with_locals, pytest.param(function_with_walrus, marks=pytest.mark.skipif(not PY38, reason='walrus appeared in 3.8')), function_with_locals_redefinition, function_with_locals_and_params, function_with_comprehension, function_with_nested, function_with_nested_and_params, method_with_locals])
def test_locals_wrong_count(assert_errors, assert_error_text, parse_ast_tree, options, code, mode):
    code = function_with_locals
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    parse_ast_tree = parse_ast_tree()
    options = options()
    mode = mode()
    '\n    Testing that local variables are counted correctly.\n\n    Regression test for #74.\n    See: https://github.com/wemake-services/wemake-python-styleguide/issues/74\n\n    Regression test for #247\n    See: https://github.com/wemake-services/wemake-python-styleguide/issues/247\n    '
    option_values = options(max_local_variables=1)
    tree = parse_ast_tree(mode(code))
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [TooManyLocalsViolation])
    assert_error_text(visitor, '2', option_values.max_local_variables)
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