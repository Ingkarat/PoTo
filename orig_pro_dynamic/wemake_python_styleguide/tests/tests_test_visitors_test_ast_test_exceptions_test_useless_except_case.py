import pytest
from wemake_python_styleguide.violations.consistency import UselessExceptCaseViolation
from wemake_python_styleguide.visitors.ast.exceptions import WrongExceptHandlerVisitor
right_empty_bare_except = '\ntry:\n    ...\nexcept:\n    ...\n'
right_logging_except = '\ntry:\n    ...\nexcept Exception:\n    sentry.log()\n    raise\n'
right_reraise_logging_except = '\ntry:\n    ...\nexcept Exception as ex:\n    sentry.log()\n    raise ex\n'
right_raise_different_except = '\ntry:\n    ...\nexcept Exception as ex:\n    raise APIException()\n'
right_raise_different_var_except = '\ntry:\n    ...\nexcept (TypeError, IndexError) as ex:\n    raise other_exception\n'
wrong_reraise_except = '\ntry:\n    ...\nexcept Exception as ex:\n    raise ex\n'
wrong_raise_except = '\ntry:\n    ...\nexcept Exception as ex:\n    raise\n'
wrong_bare_raise_except = '\ntry:\n    ...\nexcept Exception:\n    raise\n'

@pytest.mark.parametrize('code', [wrong_reraise_except, wrong_raise_except, wrong_bare_raise_except])
def test_useless_except_case(assert_errors, parse_ast_tree, code, default_options):
    code = wrong_reraise_except
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Violations are raised when using wrong except case.'
    tree = parse_ast_tree(code)
    visitor = WrongExceptHandlerVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UselessExceptCaseViolation])

@pytest.mark.parametrize('code', [right_empty_bare_except, right_logging_except, right_reraise_logging_except, right_raise_different_except, right_raise_different_var_except])
def test_correct_except_case(assert_errors, parse_ast_tree, code, default_options):
    code = right_empty_bare_except
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Violations are not raised when using correct except case.'
    tree = parse_ast_tree(code)
    visitor = WrongExceptHandlerVisitor(default_options, tree=tree)
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