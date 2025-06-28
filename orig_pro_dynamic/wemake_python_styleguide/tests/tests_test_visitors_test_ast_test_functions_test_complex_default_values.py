import pytest
from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.violations.best_practices import ComplexDefaultValueViolation, PositionalOnlyArgumentsViolation
from wemake_python_styleguide.visitors.ast.functions import FunctionSignatureVisitor
function_with_defaults = '\ndef function(arg, with_default={0}):\n    ...\n'
function_with_posonly_defaults = '\ndef function(with_default={0}, /):\n    ...\n'
function_with_kw_defaults1 = '\ndef function(*, with_default={0}):\n    ...\n'
function_with_kw_defaults2 = '\ndef function(*, arg, with_default={0}):\n    ...\n'
method_with_defaults = '\nclass Test(object):\n    def function(self, with_default={0}):\n        ...\n'
method_with_posonly_defaults = '\nclass Test(object):\n    def function(self, with_default={0}, /):\n        ...\n'
method_with_kw_defaults = '\nclass Test(object):\n    def function(self, *, with_default={0}):\n        ...\n'
lambda_with_defaults = 'lambda with_default={0}: ...'
lambda_with_posonly_defaults = 'lambda with_default={0}, /: ...'
lambda_with_kw_defaults = 'lambda *, arg, with_default={0}: ...'
all_templates = (function_with_defaults, pytest.param(function_with_posonly_defaults, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), function_with_kw_defaults1, function_with_kw_defaults2, method_with_defaults, pytest.param(method_with_posonly_defaults, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), method_with_kw_defaults, lambda_with_defaults, pytest.param(lambda_with_posonly_defaults, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), lambda_with_kw_defaults)

@pytest.mark.parametrize('template', all_templates)
@pytest.mark.parametrize('code', ["'PYFLAKES_DOCTEST' in os.environ", 'call()', 'call().attr', '-call()', '+call()', 'index[1]', 'index["s"]', 'index[name][name]', 'index[1].attr', '-index[1].attr', 'index[1].attr.call().sub', 'compare == 1', 'var + 2', 'a and b'])
def test_wrong_function_defaults(assert_errors, parse_ast_tree, default_options, template, code, mode):
    template = all_templates[0]
    code = "'PYFLAKES_DOCTEST' in os.environ"
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that wrong function defaults are forbidden.'
    tree = parse_ast_tree(mode(template.format(code)))
    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [ComplexDefaultValueViolation], ignored_types=PositionalOnlyArgumentsViolation)

@pytest.mark.parametrize('template', all_templates)
@pytest.mark.parametrize('code', ["'string'", "b''", '1', '-0', 'variable', '-variable', 'module.attr', '-module.attr', '(1, 2)', '()', 'None', 'True', 'False', '...'])
def test_correct_function_defaults(assert_errors, parse_ast_tree, default_options, template, code, mode):
    template = all_templates[0]
    code = "'string'"
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that correct function defaults passes validation.'
    tree = parse_ast_tree(mode(template.format(code)))
    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [], ignored_types=PositionalOnlyArgumentsViolation)
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