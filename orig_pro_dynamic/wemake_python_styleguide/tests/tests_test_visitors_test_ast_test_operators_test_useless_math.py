import pytest
from wemake_python_styleguide.violations.consistency import MeaninglessNumberOperationViolation
from wemake_python_styleguide.visitors.ast.operators import UselessOperatorsVisitor
usage_template = 'constant {0}'

@pytest.mark.parametrize('expression', ['*= 0', '**= -0.0', '+= 0e0', '-= -0b0', '* 0', '** -0.0', '+ 0o0', '- -0x0', '*= 1', '**= 1.0', '/= 1', '/= 0o1', '%= 1', '* 0b1', '** 1', '/ 1.0', '% 0o1', '* other / 1.0', '* 1 * other', '>> 0', '<< 0', '| 0b0', '^ 0x0', '& -0o0', '>>= 0', '<<= 0', '|= 0b0', '^= 0x0', '&= -0o0'])
def test_meaningless_math(assert_errors, parse_ast_tree, expression, default_options):
    expression = '*= 0'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that meaningless number operations are forbidden.'
    tree = parse_ast_tree(usage_template.format(expression))
    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [MeaninglessNumberOperationViolation])

@pytest.mark.parametrize('expression', ['*= -1', '*= 10', '+= 1e2', '-= -0b1', '*= 0.1', '**= 1.1', '/= 0o2', '* 0b11', '** 2', '/ -1.0', '* other / 1.5', '* -1 * other', '>> 10', '<< 1', '| 0b1', '^ 2', '^= 0x1', '& -1', '>>= 10', '<<= 1', '|= 0b1', '&= -0o1'])
def test_useful_math(assert_errors, parse_ast_tree, expression, default_options):
    expression = '*= -1'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that useful math operations are allowed.'
    tree = parse_ast_tree(usage_template.format(expression))
    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('expression', ['1 / other', '1 / 11', '1 / 1.1', '1.0 / number', '2 // other'])
def test_one_to_divide(assert_errors, parse_ast_tree, expression, default_options):
    expression = '1 / other'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that `1 / any number` is the correct expression.'
    tree = parse_ast_tree(expression)
    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('expression', ['1 / 1', '2 / 1', '3.3 / 1', 'other / 1', 'other // 1'])
def test_divide_by_one(assert_errors, parse_ast_tree, expression, default_options):
    expression = '1 / 1'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing an error when we divide by one.'
    tree = parse_ast_tree(expression)
    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [MeaninglessNumberOperationViolation])
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