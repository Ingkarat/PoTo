import pytest
from wemake_python_styleguide.violations.refactoring import SimplifiableReturningIfViolation, UselessReturningElseViolation
from wemake_python_styleguide.visitors.ast.conditions import IfStatementVisitor
function_level_condition = '\ndef function():\n    if some_condition:\n        {0}\n    else:\n        {1}\n'
for_loop_level_condition = '\ndef wrapper():\n    for _ in some_iterable:\n        if some_condition:\n            {0}\n        else:\n            {1}\n'
while_loop_level_condition = '\nwhile True:\n    if some_condition:\n        {0}\n    else:\n        {1}\n'
module_level_condition = '\nif some_condition:\n    {0}\nelse:\n    {1}\n'
multiple_ifs1 = '\ndef test():\n    parent = get_parent(node)\n    if parent is None:\n        return None\n    elif isinstance(parent, contexts):\n        {0}\n    else:\n        {1}\n'
multiple_ifs2 = '\ndef test():\n    parent = get_parent(node)\n    if parent is None:\n        {0}\n    elif isinstance(parent, contexts):\n        return None\n    else:\n        {1}\n'

@pytest.mark.parametrize('template', [function_level_condition, for_loop_level_condition, multiple_ifs1, multiple_ifs2])
@pytest.mark.parametrize('code', ['return', 'raise ValueError()'])
def test_else_that_can_be_removed_in_function(assert_errors, parse_ast_tree, code, template, default_options, mode):
    template = function_level_condition
    code = 'return'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that extra ``else`` blocks can be removed.'
    tree = parse_ast_tree(mode(template.format(code, code)))
    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UselessReturningElseViolation])

@pytest.mark.parametrize('template', [multiple_ifs1, multiple_ifs2])
@pytest.mark.parametrize('code', ['return True', 'return False'])
def test_else_that_can_be_removed_and_complex_if(assert_errors, parse_ast_tree, code, template, default_options, mode):
    template = multiple_ifs1
    code = 'return True'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that extra ``else`` blocks can be removed.'
    tree = parse_ast_tree(mode(template.format(code, code)))
    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UselessReturningElseViolation])

@pytest.mark.parametrize('template', [function_level_condition, for_loop_level_condition])
@pytest.mark.parametrize('code', ['return True', 'return False'])
def test_else_can_be_removed_and_simplifiable_if(assert_errors, parse_ast_tree, code, template, default_options, mode):
    template = function_level_condition
    code = 'return True'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Extra ``else`` blocks can be removed, plus the ``if`` is simplifiable.'
    tree = parse_ast_tree(mode(template.format(code, code)))
    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UselessReturningElseViolation, SimplifiableReturningIfViolation])

@pytest.mark.parametrize('template', [for_loop_level_condition, while_loop_level_condition])
@pytest.mark.parametrize('code', ['break', 'raise ValueError()', 'continue'])
def test_else_that_can_be_removed_in_loop(assert_errors, parse_ast_tree, template, code, default_options, mode):
    template = for_loop_level_condition
    code = 'break'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that extra ``else`` blocks can be removed.'
    tree = parse_ast_tree(mode(template.format(code, code)))
    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UselessReturningElseViolation])

@pytest.mark.parametrize('template', [module_level_condition])
@pytest.mark.parametrize('code', ['raise ValueError()'])
def test_else_that_can_be_removed_in_module(assert_errors, parse_ast_tree, template, code, default_options):
    template = module_level_condition
    code = 'raise ValueError()'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that extra ``else`` blocks can be removed.'
    tree = parse_ast_tree(template.format(code, code))
    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UselessReturningElseViolation])

@pytest.mark.parametrize('template', [function_level_condition, for_loop_level_condition, while_loop_level_condition, module_level_condition, multiple_ifs1, multiple_ifs2])
@pytest.mark.parametrize('code', ['print()', 'new_var = 1'])
def test_else_that_can_not_be_removed(assert_errors, parse_ast_tree, template, code, default_options, mode):
    template = function_level_condition
    code = 'print()'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that extra ``else`` blocks cannot be removed.'
    tree = parse_ast_tree(mode(template.format(code, 'raise ValueError()')))
    visitor = IfStatementVisitor(default_options, tree=tree)
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