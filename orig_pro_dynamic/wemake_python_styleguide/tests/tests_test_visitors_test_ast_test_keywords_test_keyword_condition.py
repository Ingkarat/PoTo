import pytest
from wemake_python_styleguide.violations.best_practices import WrongKeywordConditionViolation
from wemake_python_styleguide.visitors.ast.keywords import ConstantKeywordVisitor
while_template = '\nwhile {0}:\n    ...\n'
assert_template = 'assert {0}'
assert_with_message_template = 'assert {0}, "message"'

@pytest.mark.parametrize('code', [while_template, assert_template, assert_with_message_template])
@pytest.mark.parametrize('condition', ['0', '0.0', '+0', '-1', '--2.1', '""', 'b""', '[]', '()', '{}', 'False', 'None', '1', '0.1', '"0"', '[None]', '{1, 2, 3}', '{name: "0"}', '(a for a in some())', '[a for a in some()]', '{1 for a in some()}', '{"a": a for a in some()}', 'some if x else other'])
def test_false_condition_keywords(assert_errors, parse_ast_tree, code, condition, default_options):
    code = while_template
    condition = '0'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that false coniditions in keywords are restricted.'
    tree = parse_ast_tree(code.format(condition))
    visitor = ConstantKeywordVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [WrongKeywordConditionViolation])

@pytest.mark.parametrize('code', [assert_template, assert_with_message_template])
@pytest.mark.parametrize('condition', ['True'])
def test_false_assert_condition_keywords(assert_errors, parse_ast_tree, code, condition, default_options):
    code = assert_template
    condition = 'True'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that false coniditions in keywords are restricted.'
    tree = parse_ast_tree(code.format(condition))
    visitor = ConstantKeywordVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [WrongKeywordConditionViolation])

@pytest.mark.parametrize('code', [while_template, assert_template, assert_with_message_template])
@pytest.mark.parametrize('condition', ['call()', 'name', '-name', 'attr.value', 'attr[index]', 'method.call()', 'value in other', 'value + 1', 'x > 1', 'x + 1 > 1 and y < 1'])
def test_true_condition_keywords(assert_errors, parse_ast_tree, code, condition, default_options):
    code = while_template
    condition = 'call()'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that true coniditions in keywords are allowed.'
    tree = parse_ast_tree(code.format(condition))
    visitor = ConstantKeywordVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [while_template])
@pytest.mark.parametrize('condition', ['True'])
def test_true_while_condition_keywords(assert_errors, parse_ast_tree, code, condition, default_options):
    code = while_template
    condition = 'True'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that true coniditions in keywords are allowed.'
    tree = parse_ast_tree(code.format(condition))
    visitor = ConstantKeywordVisitor(default_options, tree=tree)
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