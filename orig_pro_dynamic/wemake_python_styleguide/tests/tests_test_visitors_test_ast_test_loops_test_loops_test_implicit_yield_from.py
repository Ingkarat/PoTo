import pytest
from wemake_python_styleguide.violations.refactoring import ImplicitYieldFromViolation
from wemake_python_styleguide.visitors.ast.loops import WrongLoopDefinitionVisitor
for_loop_template = '\ndef function():\n    for index in some:\n        {0}\n'

@pytest.mark.parametrize('template', [for_loop_template])
@pytest.mark.parametrize('code', ['yield', 'yield None', 'yield index', 'yield 10'])
def test_implicit_yield_from(assert_errors, parse_ast_tree, code, template, default_options, regular_wrapper):
    template = for_loop_template
    code = 'yield'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    regular_wrapper = regular_wrapper()
    'Ensures that implicit ``yield from`` are not allowed.'
    tree = parse_ast_tree(regular_wrapper(template.format(code)))
    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [ImplicitYieldFromViolation])

@pytest.mark.parametrize('template', [for_loop_template])
@pytest.mark.parametrize('code', ['yield', 'yield None', 'yield index', 'yield 10'])
def test_async_implicit_yield_from(assert_errors, parse_ast_tree, code, template, default_options, async_wrapper):
    template = for_loop_template
    code = 'yield'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    async_wrapper = async_wrapper()
    'Ensures that implicit ``yield from`` in async functions are allowed.'
    tree = parse_ast_tree(async_wrapper(template.format(code)))
    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('template', [for_loop_template])
@pytest.mark.parametrize('code', ['print(index)', 'yield index\n        print(index)', 'return index', 'call(index)'])
def test_correct_for_loop(assert_errors, parse_ast_tree, code, template, default_options, mode):
    template = for_loop_template
    code = 'print(index)'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Ensures that correct ``for`` loops are allowed.'
    tree = parse_ast_tree(mode(template.format(code)))
    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('template', [for_loop_template])
@pytest.mark.parametrize('code', ['yield from index'])
def test_correct_sync_for_loop(assert_errors, parse_ast_tree, code, template, default_options):
    template = for_loop_template
    code = 'yield from index'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Ensures that correct ``for`` loops are allowed.'
    tree = parse_ast_tree(template.format(code))
    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
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