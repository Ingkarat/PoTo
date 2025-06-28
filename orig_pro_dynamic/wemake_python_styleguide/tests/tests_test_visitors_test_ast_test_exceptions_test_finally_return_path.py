import pytest
from wemake_python_styleguide.violations.best_practices import TryExceptMultipleReturnPathViolation
from wemake_python_styleguide.violations.consistency import UselessExceptCaseViolation
from wemake_python_styleguide.visitors.ast.exceptions import WrongTryExceptVisitor
right_outside1 = '\ndef function():  # we need function to use ``return``\n    for _ in range(10):\n        try:\n            ...\n        except:\n            {0}\n        {0}\n'
right_outside2 = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except:\n            ...\n        {0}\n'
right_try_except = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except:\n            {0}\n'
right_try_except_multiple = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except FirstError:\n            {0}\n        except SecondError:\n            {0}\n'
right_except_else = '\ndef function():\n    for _ in range(10):\n        try:\n            ...\n        except:\n            {0}\n        else:\n            {0}\n'
right_multiple_except_else = '\ndef function():\n    for _ in range(10):\n        try:\n            ...\n        except FirstError:\n            {0}\n        except SecondError:\n            {0}\n        else:\n            {0}\n'
right_else = '\ndef function():\n    for _ in range(10):\n        try:\n            ...\n        except:\n            ...\n        else:\n            {0}\n'
right_try_except_and_else = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except:\n            {0}\n        else:\n            ...\n'
right_finally = '\ndef function():\n    for _ in range(10):\n        try:\n            ...\n        except:\n            ...\n        finally:\n            {0}\n'
right_try_catch_and_finally = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except:\n            {0}\n        finally:\n            ...\n'
right_try_catch_and_else_and_finally1 = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except:\n            {0}\n        else:\n            ...\n        finally:\n            ...\n'
right_try_catch_and_else_and_finally2 = '\ndef function():\n    for _ in range(10):\n        try:\n            ...\n        except:\n            ...\n        else:\n            ...\n        finally:\n            {0}\n'
right_try_catch_and_else_and_finally3 = '\ndef function():\n    for _ in range(10):\n        try:\n            ...\n        except:\n            {0}\n        else:\n            {0}\n        finally:\n            ...\n'
right_try_catch_and_else_and_finally4 = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except:\n            ...\n        else:\n            ...\n        finally:\n            ...\n'
wrong_try_finally = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except:\n            ...\n        finally:\n            {0}\n'
wrong_except_finally = '\ndef function():\n    for _ in range(10):\n        try:\n            ...\n        except:\n            {0}\n        finally:\n            {0}\n'
wrong_multiple_except_finally1 = '\ndef function():\n    for _ in range(10):\n        try:\n            ...\n        except FirstError:\n            {0}\n        except SecondError:\n            ...\n        finally:\n            {0}\n'
wrong_multiple_except_finally2 = '\ndef function():\n    for _ in range(10):\n        try:\n            ...\n        except FirstError:\n            ...\n        except SecondError:\n            {0}\n        finally:\n            {0}\n'
wrong_multiple_except_finally3 = '\ndef function():\n    for _ in range(10):\n        try:\n            ...\n        except FirstError:\n            {0}\n        except SecondError:\n            {0}\n        finally:\n            {0}\n'
wrong_else_finally = '\ndef function():\n    for _ in range(10):\n        try:\n            ...\n        except:\n            ...\n        else:\n            {0}\n        finally:\n            {0}\n'
wrong_try_finally = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except:\n            {0}\n        finally:\n            {0}\n'
wrong_try_else = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except:\n            ...\n        else:\n            {0}\n'
wrong_try_except_else = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except:\n            {0}\n        else:\n            {0}\n'
wrong_all1 = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except:\n            {0}\n        else:\n            {0}\n        finally:\n            {0}\n'
wrong_all2 = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except FirstError:\n            {0}\n        except SecondError:\n            {0}\n        else:\n            {0}\n        finally:\n            {0}\n'
wrong_all3 = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except FirstError:\n            ...\n        except SecondError:\n            {0}\n        else:\n            {0}\n        finally:\n            {0}\n'
wrong_all4 = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except FirstError:\n            {0}\n        except SecondError:\n            ...\n        else:\n            {0}\n        finally:\n            {0}\n'
all_nodes = '\ndef function():\n    for _ in range(10):\n        try:\n            {0}\n        except FirstError:\n            {1}\n        except SecondError:\n            {2}\n        else:\n            {3}\n        finally:\n            {4}\n'

@pytest.mark.parametrize('statement', ['return', 'return None', 'return 1', 'raise ValueError', 'raise ValueError()', 'raise TypeError(1)'])
@pytest.mark.parametrize('code', [wrong_except_finally, wrong_multiple_except_finally1, wrong_multiple_except_finally2, wrong_multiple_except_finally3, wrong_else_finally, wrong_try_finally, wrong_try_else, wrong_try_except_else, wrong_all1, wrong_all2, wrong_all3, wrong_all4])
def test_wrong_return_in_else_or_finally(assert_errors, parse_ast_tree, code, statement, default_options, mode):
    statement = 'return'
    code = wrong_except_finally
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Violations are raised when there are multiple return path.'
    tree = parse_ast_tree(mode(code.format(statement)))
    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [TryExceptMultipleReturnPathViolation], UselessExceptCaseViolation)

@pytest.mark.parametrize('statement', ['return', 'return None', 'return 1', 'raise ValueError', 'raise ValueError()', 'raise TypeError(1)'])
@pytest.mark.parametrize('code', [right_outside1, right_outside2, right_try_except, right_try_except_multiple, right_except_else, right_multiple_except_else, right_else, right_try_except_and_else, right_finally, right_try_catch_and_finally, right_try_catch_and_else_and_finally1, right_try_catch_and_else_and_finally2, right_try_catch_and_else_and_finally3, right_try_catch_and_else_and_finally4])
def test_correct_return_path_in_try_except(assert_errors, parse_ast_tree, code, statement, default_options, mode):
    statement = 'return'
    code = right_outside1
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Violations are not raised when return path is correct.'
    tree = parse_ast_tree(mode(code.format(statement)))
    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [], UselessExceptCaseViolation)

@pytest.mark.parametrize('statements', [('break', '...', '...', 'raise ValueError', '...'), ('break', '...', '...', 'return', '...'), ('return', '...', '...', 'break', '...'), ('return 0', '...', '...', 'raise ValueError', '...'), ('raise ValueError(1)', '...', '...', 'return 1', '...'), ('raise ValueError(1)', '...', '...', 'break', '...'), ('...', '...', '...', 'raise ValueError', 'return 0'), ('...', '...', '...', 'raise ValueError', 'return None'), ('...', '...', '...', 'break', 'return'), ('...', '...', '...', 'break', 'raise ValueError'), ('...', '...', '...', 'return', 'return 1'), ('...', '...', '...', 'return', 'raise ValueError()'), ('break', '...', '...', '...', 'raise ValueError'), ('break', '...', '...', '...', 'return'), ('return', '...', '...', '...', 'raise ValueError(1)'), ('return 0', '...', '...', '...', 'raise ValueError'), ('raise ValueError(1)', '...', '...', '...', 'return 1'), ('raise ValueError(1)', '...', '...', '...', 'return'), ('...', 'break', '...', '...', 'raise ValueError'), ('...', 'break', '...', '...', 'return'), ('...', 'return', '...', '...', 'raise ValueError(1)'), ('...', 'return 0', '...', '...', 'raise ValueError'), ('...', 'raise ValueError(1)', '...', '...', 'return 1'), ('...', 'raise ValueError(1)', '...', '...', 'return 0'), ('...', '...', 'break', '...', 'raise ValueError'), ('...', '...', 'break', '...', 'return'), ('...', '...', 'return', '...', 'raise ValueError'), ('...', '...', 'return 0', '...', 'raise ValueError'), ('...', '...', 'raise ValueError(1)', '...', 'return 1'), ('...', '...', 'raise ValueError(1)', '...', 'return 0')])
def test_different_nodes_trigger_violation(assert_errors, parse_ast_tree, default_options, mode, statements):
    statements = ('break', '...', '...', 'raise ValueError', '...')
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Violations are raised when there are multiple return path.'
    tree = parse_ast_tree(mode(all_nodes.format(*statements)))
    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [TryExceptMultipleReturnPathViolation])
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