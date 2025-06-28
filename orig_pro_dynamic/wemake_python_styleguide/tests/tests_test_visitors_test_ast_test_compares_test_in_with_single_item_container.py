import pytest
from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.violations.refactoring import InCompareWithSingleItemContainerViolation, WrongInCompareTypeViolation
from wemake_python_styleguide.visitors.ast.compares import InCompareSanityVisitor

@pytest.mark.parametrize('code', ['a in {1}', 'a in {1: "a"}', 'a in [1]', 'a in (1,)', 'a in "a"', 'a in b"a"', 'a in {*a}', 'a in {**a}', pytest.param('a in (x := [1])', marks=pytest.mark.skipif(not PY38, reason='walrus appeared in 3.8'))])
def test_single_item_container(assert_errors, parse_ast_tree, code, default_options, in_not_in):
    code = 'a in {1}'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    in_not_in = in_not_in()
    'Compares forbid ``in`` with single item containers.'
    tree = parse_ast_tree(code)
    visitor = InCompareSanityVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [InCompareWithSingleItemContainerViolation], ignored_types=(WrongInCompareTypeViolation,))

@pytest.mark.parametrize('code', ['a in {1, 2}', 'a in {1: "a", 2: "b"}', 'a in [1, 2]', 'a in (1, 2)', 'a in "ab"', 'a in {1, *a}', 'a in {1: "a", **a}', pytest.param('a in (x := {1, 2, 3})', marks=pytest.mark.skipif(not PY38, reason='walrus appeared in 3.8'))])
def test_multi_item_container(assert_errors, parse_ast_tree, code, default_options, in_not_in):
    code = 'a in {1, 2}'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    in_not_in = in_not_in()
    'Compares allow ``in`` with multi items containers.'
    tree = parse_ast_tree(code)
    visitor = InCompareSanityVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [], ignored_types=(WrongInCompareTypeViolation,))
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
if_with_is = 'if {0} is {1}: ...'
if_with_is_not = 'if {0} is not {1}: ...'
if_with_eq = 'if {0} == {1}: ...'
if_with_not_eq = 'if {0} != {1}: ...'
assert_construct = 'assert {0} == {1}'
assert_with_message = 'assert {0} == {1}, "message"'
if_with_gt = 'if {0} > {1}: ...'
if_with_lt = 'if {0} < {1}: ...'
if_with_gte = 'if {0} >= {1}: ...'
if_with_lte = 'if {0} <= {1}: ...'
if_with_chained_compares1 = 'if 0 < {0} < {1}: ...'
if_with_chained_compares2 = 'if {0} > {1} > 0: ...'
if_with_chained_compares3 = 'if -1 > {0} > {1} > 0: ...'
if_with_in = 'if {0} in {1}: ...'
if_with_not_in = 'if {0} not in {1}: ...'
ternary = 'ternary = 0 if {0} > {1} else 1'
while_construct = 'while {0} > {1}: ...'
IS_COMPARES = frozenset((if_with_is, if_with_is_not))
EQUAL_COMPARES = frozenset((if_with_eq, if_with_not_eq, assert_construct, assert_with_message))
OTHER_COMPARES = frozenset((if_with_lt, if_with_gt, if_with_lte, if_with_gte, ternary, while_construct))

@pytest.fixture(params=IS_COMPARES | EQUAL_COMPARES | OTHER_COMPARES)
def simple_conditions(request):
    """Fixture that returns simple conditionals."""
    return request.param
    'Fixture that returns simple conditionals.'
    return (IS_COMPARES | EQUAL_COMPARES | OTHER_COMPARES)[0]

@pytest.fixture(params=IS_COMPARES)
def is_conditions(request):
    """Fixture that returns `is` and `is not` conditionals."""
    return request.param
    'Fixture that returns `is` and `is not` conditionals.'
    return IS_COMPARES[0]

@pytest.fixture(params=EQUAL_COMPARES)
def eq_conditions(request):
    """Fixture that returns `eq` and `not eq` conditionals."""
    return request.param
    'Fixture that returns `eq` and `not eq` conditionals.'
    return EQUAL_COMPARES[0]

@pytest.fixture(params=OTHER_COMPARES)
def other_conditions(request):
    """Fixture that returns other compare conditionals."""
    return request.param
    'Fixture that returns other compare conditionals.'
    return OTHER_COMPARES[0]

@pytest.fixture(params=[if_with_in, if_with_not_in])
def in_conditions(request):
    """Fixture that returns simple conditionals."""
    return request.param
    'Fixture that returns simple conditionals.'
    return [if_with_in, if_with_not_in][0]

@pytest.fixture()
def not_in_wrapper():
    """Fixture to replace all `in` operators to `not in` operators."""

    def factory(template: str) -> str:
        return template.replace(' in ', ' not in ')
    return factory

@pytest.fixture(params=['not_in_wrapper', 'regular_wrapper'])
def in_not_in(request):
    """Fixture that returns either `not in` or `in` operators."""
    return request.getfixturevalue(request.param)