from wemake_python_styleguide.violations.complexity import TooManyArgumentsViolation
from wemake_python_styleguide.visitors.ast.complexity.function import FunctionComplexityVisitor

def test_correct_arguments_count(assert_errors, parse_ast_tree, single_argument, default_options, mode):
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    single_argument = single_argument()
    default_options = default_options()
    mode = mode()
    'Ensures that functions with correct argument count works.'
    tree = parse_ast_tree(mode(single_argument))
    visitor = FunctionComplexityVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

def test_single_argument_count(assert_errors, parse_ast_tree, single_argument, options, mode):
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    single_argument = single_argument()
    options = options()
    mode = mode()
    'Ensures that functions with correct argument count works.'
    tree = parse_ast_tree(mode(single_argument))
    option_values = options(max_arguments=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

def test_no_arguments(assert_errors, parse_ast_tree, options, mode):
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    options = options()
    mode = mode()
    'Ensures that functions with no arguments work.'
    tree = parse_ast_tree(mode('def function(): ...'))
    option_values = options(max_arguments=0)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

def test_single_argument_count_invalid(assert_errors, assert_error_text, parse_ast_tree, single_argument, options, mode):
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    parse_ast_tree = parse_ast_tree()
    single_argument = single_argument()
    options = options()
    mode = mode()
    'Ensures that functions raise violation when there are multiple args.'
    tree = parse_ast_tree(mode(single_argument))
    option_values = options(max_arguments=0)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [TooManyArgumentsViolation])
    assert_error_text(visitor, '1', option_values.max_arguments)

def test_two_arguments_count_invalid(assert_errors, assert_error_text, parse_ast_tree, two_arguments, options, mode):
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    parse_ast_tree = parse_ast_tree()
    two_arguments = two_arguments()
    options = options()
    mode = mode()
    'Ensures that functions raise violation when there are multiple args.'
    tree = parse_ast_tree(mode(two_arguments))
    option_values = options(max_arguments=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [TooManyArgumentsViolation])
    assert_error_text(visitor, '2', option_values.max_arguments)
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
from wemake_python_styleguide.compat.constants import PY38
function_with_single_argument = 'def function(arg1): ...'
function_with_arguments = 'def function(arg1, arg2): ...'
function_with_args_kwargs = 'def function(*args, **kwargs): ...'
function_with_kwonly = 'def function(*, kwonly1, kwonly2=True): ...'
function_with_posonly = 'def function(arg1, arg2, /): ...'
method_without_arguments = '\nclass Test(object):\n    def method(self): ...\n'
method_with_single_argument = '\nclass Test(object):\n    def method(self, arg): ...\n'
method_with_single_args = '\nclass Test(object):\n    def method(self, *args): ...\n'
method_with_single_posonly_arg = '\nclass Test(object):\n    def method(self, arg, /): ...\n'
method_with_single_kwargs = '\nclass Test(object):\n    def method(self, **kwargs): ...\n'
method_with_single_kwonly = '\nclass Test(object):\n    def method(self, *, kwonly=True): ...\n'
classmethod_without_arguments = '\nclass Test(object):\n    @classmethod\n    def method(cls): ...\n'
classmethod_with_single_argument = '\nclass Test(object):\n    @classmethod\n    def method(cls, arg1): ...\n'
new_method_without_arguments = '\nclass Test(object):\n    def __new__(cls): ...\n'
new_method_single_argument = '\nclass Test(object):\n    def __new__(cls, arg1): ...\n'
metaclass_without_arguments = '\nclass TestMeta(type):\n    def method(cls): ...\n'
metaclass_with_single_argument = '\nclass TestMeta(type):\n    def method(cls, arg1): ...\n'

@pytest.fixture(params=[function_with_single_argument, method_without_arguments, classmethod_without_arguments, new_method_without_arguments, metaclass_without_arguments])
def single_argument(request):
    """Fixture that returns different code examples that have one arg."""
    return request.param
    'Fixture that returns different code examples that have one arg.'
    return [function_with_single_argument, method_without_arguments, classmethod_without_arguments, new_method_without_arguments, metaclass_without_arguments][0]

@pytest.fixture(params=[function_with_arguments, function_with_args_kwargs, function_with_kwonly, pytest.param(function_with_posonly, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), method_with_single_argument, method_with_single_args, method_with_single_kwargs, method_with_single_kwonly, pytest.param(method_with_single_posonly_arg, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), classmethod_with_single_argument, new_method_single_argument, metaclass_with_single_argument])
def two_arguments(request):
    """Fixture that returns different code examples that have two args."""
    return request.param
    'Fixture that returns different code examples that have two args.'
    return [function_with_arguments, function_with_args_kwargs, function_with_kwonly, pytest.param(function_with_posonly, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), method_with_single_argument, method_with_single_args, method_with_single_kwargs, method_with_single_kwonly, pytest.param(method_with_single_posonly_arg, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), classmethod_with_single_argument, new_method_single_argument, metaclass_with_single_argument][0]
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
import pytest
from wemake_python_styleguide.compat.constants import PY38
function_with_single_argument = 'def function(arg1): ...'
function_with_arguments = 'def function(arg1, arg2): ...'
function_with_args_kwargs = 'def function(*args, **kwargs): ...'
function_with_kwonly = 'def function(*, kwonly1, kwonly2=True): ...'
function_with_posonly = 'def function(arg1, arg2, /): ...'
method_without_arguments = '\nclass Test(object):\n    def method(self): ...\n'
method_with_single_argument = '\nclass Test(object):\n    def method(self, arg): ...\n'
method_with_single_args = '\nclass Test(object):\n    def method(self, *args): ...\n'
method_with_single_posonly_arg = '\nclass Test(object):\n    def method(self, arg, /): ...\n'
method_with_single_kwargs = '\nclass Test(object):\n    def method(self, **kwargs): ...\n'
method_with_single_kwonly = '\nclass Test(object):\n    def method(self, *, kwonly=True): ...\n'
classmethod_without_arguments = '\nclass Test(object):\n    @classmethod\n    def method(cls): ...\n'
classmethod_with_single_argument = '\nclass Test(object):\n    @classmethod\n    def method(cls, arg1): ...\n'
new_method_without_arguments = '\nclass Test(object):\n    def __new__(cls): ...\n'
new_method_single_argument = '\nclass Test(object):\n    def __new__(cls, arg1): ...\n'
metaclass_without_arguments = '\nclass TestMeta(type):\n    def method(cls): ...\n'
metaclass_with_single_argument = '\nclass TestMeta(type):\n    def method(cls, arg1): ...\n'

@pytest.fixture(params=[function_with_single_argument, method_without_arguments, classmethod_without_arguments, new_method_without_arguments, metaclass_without_arguments])
def single_argument(request):
    """Fixture that returns different code examples that have one arg."""
    return request.param
    'Fixture that returns different code examples that have one arg.'
    return [function_with_single_argument, method_without_arguments, classmethod_without_arguments, new_method_without_arguments, metaclass_without_arguments][0]

@pytest.fixture(params=[function_with_arguments, function_with_args_kwargs, function_with_kwonly, pytest.param(function_with_posonly, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), method_with_single_argument, method_with_single_args, method_with_single_kwargs, method_with_single_kwonly, pytest.param(method_with_single_posonly_arg, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), classmethod_with_single_argument, new_method_single_argument, metaclass_with_single_argument])
def two_arguments(request):
    """Fixture that returns different code examples that have two args."""
    return request.param
    'Fixture that returns different code examples that have two args.'
    return [function_with_arguments, function_with_args_kwargs, function_with_kwonly, pytest.param(function_with_posonly, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), method_with_single_argument, method_with_single_args, method_with_single_kwargs, method_with_single_kwonly, pytest.param(method_with_single_posonly_arg, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), classmethod_with_single_argument, new_method_single_argument, metaclass_with_single_argument][0]