import pytest
from wemake_python_styleguide.violations.consistency import UselessNodeViolation
from wemake_python_styleguide.visitors.ast.statements import StatementsWithBodiesVisitor
for_template = '\ndef wrapper():\n    for some_var in call():\n        {0}\n'
while_template = '\ndef wrapper():\n    while True:\n        {0}\n'
with_template = '\ndef wrapper():\n    for wrapping_loop in []:\n        with some():\n            {0}\n'
try_template = '\ndef wrapper():\n    for wrapping_loop in []:\n        try:\n            {0}\n        except Exception:\n            some_call()\n'

@pytest.mark.parametrize('code', [for_template, while_template, with_template, try_template])
@pytest.mark.parametrize('statement', ['break', 'continue', 'pass'])
def test_useless_nodes(assert_errors, parse_ast_tree, code, statement, default_options, mode):
    code = for_template
    statement = 'break'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Ensures that useless nodes are forbidden.'
    tree = parse_ast_tree(mode(code.format(statement)))
    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UselessNodeViolation])

@pytest.mark.parametrize('code', [for_template, while_template])
@pytest.mark.parametrize('statement', ['return 1', 'raise TypeError()'])
def test_useless_loop_nodes(assert_errors, parse_ast_tree, code, statement, default_options, mode):
    code = for_template
    statement = 'return 1'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Ensures that useless loop nodes are forbidden.'
    tree = parse_ast_tree(mode(code.format(statement)))
    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UselessNodeViolation])

@pytest.mark.parametrize('code', [try_template])
@pytest.mark.parametrize('statement', ['raise TypeError()'])
def test_useless_try_nodes(assert_errors, assert_error_text, parse_ast_tree, code, statement, default_options, mode):
    code = try_template
    statement = 'raise TypeError()'
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Ensures that useless try nodes are forbidden.'
    tree = parse_ast_tree(mode(code.format(statement)))
    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UselessNodeViolation])
    assert_error_text(visitor, 'try')

@pytest.mark.parametrize('code', [for_template, while_template, with_template, try_template])
@pytest.mark.parametrize('statement', ['some_var = 1', 'some_call()'])
def test_useful_nodes(assert_errors, parse_ast_tree, code, statement, default_options, mode):
    code = for_template
    statement = 'some_var = 1'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Ensures that useful nodes are required.'
    tree = parse_ast_tree(mode(code.format(statement)))
    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
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