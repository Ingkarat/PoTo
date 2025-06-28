import pytest
from wemake_python_styleguide.violations.best_practices import MultipleAssignmentsViolation, WrongUnpackingViolation
from wemake_python_styleguide.violations.consistency import UnpackingIterableToListViolation
from wemake_python_styleguide.visitors.ast.builtins import WrongAssignmentVisitor
list_target = '[first, second]'
nested_list_target0 = '([first, second], third)'
nested_list_target1 = '(first, [second, third])'
nested_list_target2 = '(first, (second, [third, fourth]))'
multiple_level_nested_list_target = '(first, (second, [third, fourth]))'
spread_assignment_in_list_target = '[first, *rest]'
nested_spread_assignment_in_list = '(first, [second, *rest])'
multiple_level_nested_spread_assign_in_list = '(first, (second, [*rest, last]))'
regular_assignment = '{0} = some()'
regular_multiple_assignment = 'result = {0} = some_other_result = some()'
for_assignment = '\ndef wrapper():\n    for {0} in iterable:\n        ...\n'
list_comprehension = '\ndef wrapper():\n    comp = [1 for {0} in some()]\n'
generator_expression = '\ndef wrapper():\n    comp = (1 for {0} in some())\n'
set_comprehension = '\ndef wrapper():\n    comp = {{1 for {0} in some()}}\n'
dict_comprehension = "\ndef wrapper():\n    comp = {{'1': 1 for {0} in some()}}\n"
with_assignment = '\ndef wrapper():\n    with some() as {0}:\n        ...\n'
with_multiple_assignments = '\ndef wrapper():\n    with some() as s, some_other() as {0} :\n        ...\n'

@pytest.mark.parametrize('assignment', [list_target, spread_assignment_in_list_target])
@pytest.mark.parametrize('code', [regular_assignment, for_assignment, list_comprehension, generator_expression, set_comprehension, dict_comprehension, with_assignment, with_multiple_assignments])
def test_unpacking_to_list(assert_errors, parse_ast_tree, default_options, code, assignment):
    assignment = list_target
    code = regular_assignment
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Ensure that unpacking iterable to list is restricted.'
    tree = parse_ast_tree(code.format(assignment))
    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UnpackingIterableToListViolation])

@pytest.mark.parametrize('assignment', [nested_list_target0, nested_list_target1, nested_list_target2, multiple_level_nested_list_target, nested_spread_assignment_in_list, multiple_level_nested_spread_assign_in_list])
@pytest.mark.parametrize('code', [regular_assignment, for_assignment, list_comprehension, generator_expression, set_comprehension, dict_comprehension, with_assignment, with_multiple_assignments])
def test_unpacking_to_nested_list(assert_errors, parse_ast_tree, default_options, code, assignment):
    assignment = nested_list_target0
    code = regular_assignment
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Ensure that unpacking iterable to nested list is restricted.'
    tree = parse_ast_tree(code.format(assignment))
    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UnpackingIterableToListViolation, WrongUnpackingViolation])

@pytest.mark.parametrize('assignment', [list_target, nested_list_target0, nested_list_target1, nested_list_target2, multiple_level_nested_list_target, spread_assignment_in_list_target, nested_spread_assignment_in_list, multiple_level_nested_spread_assign_in_list])
@pytest.mark.parametrize('code', [regular_multiple_assignment])
def test_unpacking_to_list_in_middle_target(assert_errors, parse_ast_tree, default_options, code, assignment):
    assignment = list_target
    code = regular_multiple_assignment
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Ensure that unpacking iterable to list in middle target is restricted.'
    tree = parse_ast_tree(code.format(assignment))
    visitor = WrongAssignmentVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [MultipleAssignmentsViolation, UnpackingIterableToListViolation])
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