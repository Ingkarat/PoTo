import pytest
from wemake_python_styleguide.violations.best_practices import SingleElementDestructuringViolation, WrongUnpackingViolation
from wemake_python_styleguide.violations.consistency import UnpackingIterableToListViolation
from wemake_python_styleguide.visitors.ast.builtins import WrongAssignmentVisitor
single_assignment = '{0} = 1'
sequence_assignment1 = 'first, {0} = {1}'
sequence_assignment2 = '{0}, second = {1}'
tuple_assignment1 = 'first, {0} = (1, 2)'
tuple_assignment2 = '{0}, second = (1, 2)'
spread_assignment1 = '{0}, *second = [1, 2, 3]'
spread_assignment2 = 'first, *{0} = [1, 2, 3]'
for_assignment = '\ndef wrapper():\n    for {0} in []:\n        ...\n'
for_unpacking1 = '\ndef wrapper():\n    for {0}, second in enumerate([]):\n        ...\n'
for_unpacking2 = '\ndef wrapper():\n    for first, {0} in enumerate([]):\n        ...\n'
list_comprehension = '\ndef wrapper():\n    comp = [1 for first, {0} in enumerate([])]\n'
dict_comprehension = "\ndef wrapper():\n    comp = {{'1': 1 for first, {0} in enumerate([])}}\n"
set_comprehension = '\ndef wrapper():\n    comp = {{1 for {0}, second in enumerate([])}}\n'
generator_expression = '\ndef wrapper():\n    comp = (1 for first, {0} in enumerate([]))\n'
with_assignment = '\ndef wrapper():\n    with some() as {0}:\n        ...\n'
with_unpacking1 = '\ndef wrapper():\n    with some() as ({0}, second):\n        ...\n'
with_unpacking2 = '\ndef wrapper():\n    with some() as (first, {0}):\n        ...\n'
correct_single_destructuring = 'first = {0}'
wrong_single_destructuring1 = 'first, = {0}'
wrong_single_destructuring2 = '(first,) = {0}'
wrong_single_destructuring3 = '[first] = {0}'

@pytest.mark.parametrize('code', [single_assignment, sequence_assignment1, sequence_assignment2, tuple_assignment1, tuple_assignment2, spread_assignment1, spread_assignment2, for_assignment, for_unpacking1, for_unpacking2, list_comprehension, dict_comprehension, set_comprehension, generator_expression, with_assignment, with_unpacking1, with_unpacking2])
@pytest.mark.parametrize('target', ['(1, 2)', '[1, 2]'])
def test_correct_unpacking(assert_errors, parse_ast_tree, code, target, default_options, mode):
    code = single_assignment
    target = '(1, 2)'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that correct assignments work.'
    tree = parse_ast_tree(mode(code.format('some_name', target)))
    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('assignment', ['some[0]', 'some["key"]', 'some.attr'])
def test_correct_assignment(assert_errors, parse_ast_tree, assignment, default_options, mode):
    assignment = 'some[0]'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that correct assignments work.'
    tree = parse_ast_tree(mode(single_assignment.format(assignment)))
    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [sequence_assignment1, sequence_assignment2, tuple_assignment1, tuple_assignment2, spread_assignment1, spread_assignment2, for_unpacking1, for_unpacking2, list_comprehension, dict_comprehension, set_comprehension, generator_expression, with_unpacking1, with_unpacking2])
@pytest.mark.parametrize('assignment', ['some[0]', 'some["key"]', 'some[obj]', 'some.attr', 'some[0]["key"]', 'some["key"][0]'])
@pytest.mark.parametrize('target', ['(1, 2)', '[1, 2]'])
def test_multiple_assignments(assert_errors, parse_ast_tree, code, target, assignment, default_options, mode):
    code = sequence_assignment1
    assignment = 'some[0]'
    target = '(1, 2)'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that multiple assignments are restricted.'
    tree = parse_ast_tree(mode(code.format(assignment, target)))
    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [WrongUnpackingViolation])

@pytest.mark.parametrize('target', ['(1,)[0]', '[1][0]'])
def test_correct_destructing(assert_errors, parse_ast_tree, target, default_options, mode):
    target = '(1,)[0]'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that correct elements destructuring work.'
    tree = parse_ast_tree(mode(correct_single_destructuring.format(target)))
    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [wrong_single_destructuring1, wrong_single_destructuring2, wrong_single_destructuring3])
@pytest.mark.parametrize('assignment', ['(1,)', '[1]', 'some', 'some()'])
def test_single_element_destructing(assert_errors, parse_ast_tree, code, assignment, default_options, mode):
    code = wrong_single_destructuring1
    assignment = '(1,)'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that single element destructuring is restricted.'
    tree = parse_ast_tree(mode(code.format(assignment)))
    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [SingleElementDestructuringViolation], ignored_types=UnpackingIterableToListViolation)
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