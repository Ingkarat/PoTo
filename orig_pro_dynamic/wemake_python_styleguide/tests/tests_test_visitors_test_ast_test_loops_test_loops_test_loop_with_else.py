import pytest
from wemake_python_styleguide.violations.refactoring import UselessLoopElseViolation
from wemake_python_styleguide.visitors.ast.loops import WrongLoopVisitor
wrong_else_in_for_loop = "\ndef wrapper():\n    for x in '123':\n        ...\n    else:\n        ...\n"
wrong_nested_else_in_for_loop = "\ndef wrapper():\n    for letters in ['abc', 'zxc', 'rrd']:\n        for x in letters:\n            ...\n        else:\n            ...\n"
wrong_nested_for_with_break = "\ndef wrapper():\n    for letters in ['abc', 'zxc', 'rrd']:\n        for x in letters:\n            break\n    else:\n        ...\n"
wrong_nested_while_with_break = "\ndef wrapper():\n    for letters in ['abc', 'zxc', 'rrd']:\n        while 'a' in letters:\n            break\n    else:\n        ...\n"
wrong_multiple_breaks = "\ndef wrapper():\n    for x in 'zzz':\n        for i in range(10):\n            if i > 1:\n                break\n        else:\n            break\n    else:\n        ...\n"
wrong_while_without_break = '\nwhile x > 2:\n    ...\nelse:\n    ...\n'
right_else_in_for_loop = "\ndef wrapper():\n    for x in '123':\n        break\n    else:\n        ...\n"
right_multiple_breaks = "\ndef wrapper():\n    for x in 'xxx':\n        for i in range(10):\n            if i > 1:\n                break\n        break\n    else:\n        ...\n"
right_multiple_nested_for_with_break = "\ndef wrapper():\n    for letters in ['abc', 'zxc', 'rrd']:\n        for x in letters:\n            break\n\n        for y in letters:\n            break\n\n        while letters:\n            break\n    else:\n        ...\n"
right_nested_break_in_for_loop = "\ndef wrapper():\n    for x in 'nnn':\n        if x == '1':\n            break\n    else:\n        ...\n"
right_nested_if_else = "\ndef wrapper():\n    for x in '000':\n        if x:\n            ...\n        else:\n            ...\n"
right_while_with_break = '\nwhile x > 2:\n    break\nelse:\n    ...\n'
right_while_without_break_and_else = '\nwhile x > 2:\n    ...\n'

@pytest.mark.parametrize('code', [wrong_else_in_for_loop, wrong_nested_else_in_for_loop, wrong_nested_for_with_break, wrong_nested_while_with_break, wrong_multiple_breaks, wrong_while_without_break])
def test_wrong_else_in_for_loop(assert_errors, parse_ast_tree, code, default_options, mode):
    code = wrong_else_in_for_loop
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Violations are raised when else with break statement.'
    tree = parse_ast_tree(mode(code))
    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UselessLoopElseViolation])

@pytest.mark.parametrize('code', [right_else_in_for_loop, right_nested_break_in_for_loop, right_multiple_nested_for_with_break, right_multiple_breaks, right_nested_if_else, right_while_with_break, right_while_without_break_and_else])
def test_correct_else_in_for_loop(assert_errors, parse_ast_tree, code, default_options, mode):
    code = right_else_in_for_loop
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Violations are not raised when else without break statement.'
    tree = parse_ast_tree(mode(code))
    visitor = WrongLoopVisitor(default_options, tree=tree)
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