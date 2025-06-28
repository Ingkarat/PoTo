import pytest
from wemake_python_styleguide.violations.best_practices import BlockAndLocalOverlapViolation
from wemake_python_styleguide.visitors.ast.blocks import BlockVariableVisitor
function_def1 = 'def {0}():'
function_template1 = '\n{0}\n    ...\n\n{1}\n'
function_template2 = '\n{1}\n\n{0}\n    ...\n'
method_template1 = '\n{1}\n\nclass Test(object):\n    {0}\n        ...\n'
method_template2 = '\nclass Test(object):\n    {0}\n        ...\n\n{1}\n'

@pytest.mark.parametrize('function_statement', [function_def1])
@pytest.mark.parametrize('context', [function_template1, function_template2])
@pytest.mark.parametrize('variable_name', ['should_raise'])
def test_function_block_overlap(assert_errors, assert_error_text, parse_ast_tree, function_statement, assign_statement, context, variable_name, default_options, mode):
    function_statement = function_def1
    context = function_template1
    variable_name = 'should_raise'
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    parse_ast_tree = parse_ast_tree()
    assign_statement = assign_statement()
    default_options = default_options()
    mode = mode()
    'Ensures that overlapping variables exist.'
    code = context.format(function_statement.format(variable_name), assign_statement.format(variable_name))
    tree = parse_ast_tree(mode(code))
    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [BlockAndLocalOverlapViolation])
    assert_error_text(visitor, variable_name)

@pytest.mark.parametrize('function_statement', [function_def1])
@pytest.mark.parametrize('context', [method_template1, method_template2])
@pytest.mark.parametrize('variable_name', ['should_raise'])
def test_method_block_overlap(assert_errors, parse_ast_tree, function_statement, assign_and_annotation_statement, context, variable_name, default_options, mode):
    function_statement = function_def1
    context = method_template1
    variable_name = 'should_raise'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    assign_and_annotation_statement = assign_and_annotation_statement()
    default_options = default_options()
    mode = mode()
    'Ensures that overlapping variables exist.'
    code = context.format(function_statement.format(variable_name), assign_and_annotation_statement.format(variable_name))
    tree = parse_ast_tree(mode(code))
    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('function_statement', [function_def1])
@pytest.mark.parametrize('context', [function_template1, function_template2, method_template1, method_template2])
@pytest.mark.parametrize('variable_name', ['should_raise'])
def test_function_block_usage(assert_errors, parse_ast_tree, function_statement, context, variable_name, default_options, mode):
    function_statement = function_def1
    context = function_template1
    variable_name = 'should_raise'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Ensures using variables is fine.'
    code = context.format(function_statement.format(variable_name), 'print({0})'.format(variable_name))
    tree = parse_ast_tree(mode(code))
    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('function_statement', [function_def1])
@pytest.mark.parametrize('context', [function_template1, function_template2, method_template1, method_template2])
@pytest.mark.parametrize(('first_name', 'second_name'), [('unique_name', 'unique_name1'), ('_', '_')])
def test_function_block_correct(assert_errors, parse_ast_tree, function_statement, assign_and_annotation_statement, context, first_name, second_name, default_options, mode):
    function_statement = function_def1
    context = function_template1
    (first_name, second_name) = ('unique_name', 'unique_name1')
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    assign_and_annotation_statement = assign_and_annotation_statement()
    default_options = default_options()
    mode = mode()
    'Ensures that different variables do not overlap.'
    code = context.format(function_statement.format(first_name), assign_and_annotation_statement.format(second_name))
    tree = parse_ast_tree(mode(code))
    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])
pipeline = '\ndef pipeline(function):\n    return\n'
overload_template = '\n{0}\n{1}\n{1}\n'

@pytest.mark.parametrize('import_overload', ['@overload', '@typing.overload'])
def test_function_overload(assert_errors, assert_error_text, parse_ast_tree, default_options, import_overload, mode):
    import_overload = '@overload'
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Ensures that overload from typing do not overlap.'
    code = overload_template.format(import_overload, pipeline)
    tree = parse_ast_tree(mode(code))
    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('decorator_template', ['@typing.func', '@module.overload', '@decorate'])
def test_no_function_overload(assert_errors, assert_error_text, parse_ast_tree, default_options, decorator_template, mode):
    decorator_template = '@typing.func'
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Ensures that not overload from typing do overlap.'
    code = overload_template.format(decorator_template, pipeline)
    tree = parse_ast_tree(mode(code))
    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [BlockAndLocalOverlapViolation])
method_setter_template = '\nclass Test(object):\n    @property\n    def {0}():\n        ...\n    @{0}.setter\n    def {0}():\n        {0} = ...\n'

def test_property_setter(assert_errors, parse_ast_tree, default_options, mode):
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Ensures that property setter do not overlap.'
    code = method_setter_template.format('func')
    tree = parse_ast_tree(mode(code))
    visitor = BlockVariableVisitor(default_options, tree=tree)
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
import pytest
simple_assign = '{0} = 1'
multiple_assign = '{0} = unmatched_assign = 1'
annotated_assign1 = '{0}: type = 1'
simple_annotation = '{0}: type'
unpacking_assign1 = '{0}, unmatched_assign = (1, 2)'
unpacking_assign2 = 'unmatched_assign, *{0} = (1, 2)'
_assigned_statements = [simple_assign, multiple_assign, annotated_assign1, unpacking_assign1, unpacking_assign2]
_assigned_and_annotation_statements = _assigned_statements + [simple_annotation]

@pytest.fixture(params=_assigned_statements)
def assign_statement(request):
    """Parametrized fixture that contains all possible assign templates."""
    return request.param
    'Parametrized fixture that contains all possible assign templates.'
    return _assigned_statements[0]

@pytest.fixture(params=_assigned_and_annotation_statements)
def assign_and_annotation_statement(request):
    """Parametrized fixture that contains all possible assign templates."""
    return request.param
    'Parametrized fixture that contains all possible assign templates.'
    return _assigned_and_annotation_statements[0]
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
import pytest
simple_assign = '{0} = 1'
multiple_assign = '{0} = unmatched_assign = 1'
annotated_assign1 = '{0}: type = 1'
simple_annotation = '{0}: type'
unpacking_assign1 = '{0}, unmatched_assign = (1, 2)'
unpacking_assign2 = 'unmatched_assign, *{0} = (1, 2)'
_assigned_statements = [simple_assign, multiple_assign, annotated_assign1, unpacking_assign1, unpacking_assign2]
_assigned_and_annotation_statements = _assigned_statements + [simple_annotation]

@pytest.fixture(params=_assigned_statements)
def assign_statement(request):
    """Parametrized fixture that contains all possible assign templates."""
    return request.param
    'Parametrized fixture that contains all possible assign templates.'
    return _assigned_statements[0]

@pytest.fixture(params=_assigned_and_annotation_statements)
def assign_and_annotation_statement(request):
    """Parametrized fixture that contains all possible assign templates."""
    return request.param
    'Parametrized fixture that contains all possible assign templates.'
    return _assigned_and_annotation_statements[0]