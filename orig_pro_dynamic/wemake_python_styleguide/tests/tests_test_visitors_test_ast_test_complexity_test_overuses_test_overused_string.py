import pytest
from wemake_python_styleguide.violations.complexity import OverusedStringViolation
from wemake_python_styleguide.visitors.ast.complexity.overuses import StringOveruseVisitor
string_actions = '\nfirst = {0}\nsecond({0})\nthird[{0}]\n\'new\' + {0}\n{0}.join("1", "2", "3")\n'
string_function_type_annotations1 = '\ndef first(\n    arg1: {0},\n    arg2: {0},\n    arg3: {0},\n    arg4: {0},\n) -> {0}:\n    ...\n'
string_function_type_annotations2 = '\ndef func1() -> {0}:\n    ...\n\ndef func2() -> {0}:\n    ...\n\ndef func3() -> {0}:\n    ...\n\ndef func4() -> {0}:\n    ...\n'
string_class_type_annotations = '\nclass SomeClass(object):\n    first: {0}\n    second: {0}\n    third: {0}\n    fourth: {0}\n'
string_method_type_annotations1 = '\nclass SomeClass(object):\n    def first(\n        self,\n        arg1: {0},\n        arg2: {0},\n        arg3: {0},\n        arg4: {0},\n    ) -> {0}:\n        ...\n'
string_method_type_annotations2 = '\nclass SomeClass(object):\n    def method1(self) -> {0}:\n        ...\n\n    def method2(self) -> {0}:\n        ...\n\n    def method3(self) -> {0}:\n        ...\n\n    def method4(self) -> {0}:\n        ...\n'
string_variable_type_annotations = '\nfirst: {0}\nsecond: {0}\nthird: {0}\nfourth: {0}\n'
regression1127 = '\nfirst: List[{0}]\n\nclass Some(object):\n    field: {0}\n\n    def method(self, arg: {0}):\n        ...\n\ndef function() -> Dict[int, {0}]:\n    ...\n'

@pytest.mark.parametrize('strings', [string_actions, string_function_type_annotations1, string_function_type_annotations2, string_class_type_annotations, string_method_type_annotations1, string_method_type_annotations2, string_variable_type_annotations, regression1127])
@pytest.mark.parametrize('string_value', ['"same_string"', '"GenericType[int, str]"'])
def test_string_overuse_settings(assert_errors, parse_ast_tree, options, strings, string_value, mode):
    strings = string_actions
    string_value = '"same_string"'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    options = options()
    mode = mode()
    'Ensures that settings for string over-use work.'
    tree = parse_ast_tree(mode(strings.format(string_value)))
    option_values = options(max_string_usages=5)
    visitor = StringOveruseVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('strings', [string_actions])
@pytest.mark.parametrize('string_value', ['"same-string"', '"GenericType[int, str]"'])
@pytest.mark.parametrize('prefix', ['b', 'u', ''])
def test_string_overuse(assert_errors, assert_error_text, parse_ast_tree, default_options, strings, prefix, string_value):
    strings = string_actions
    string_value = '"same-string"'
    prefix = 'b'
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Ensures that over-used strings raise violations.'
    tree = parse_ast_tree(strings.format(prefix + string_value))
    visitor = StringOveruseVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [OverusedStringViolation])
    assert_error_text(visitor, string_value.replace('"', '') or "''", default_options.max_string_usages)

@pytest.mark.parametrize('strings', [string_function_type_annotations1, string_function_type_annotations2, string_class_type_annotations, string_method_type_annotations1, string_method_type_annotations2, string_variable_type_annotations, regression1127])
@pytest.mark.parametrize('string_value', ['"GenericType[int, str]"', '"int"', 'List["int"]'])
def test_string_type_annotations(assert_errors, parse_ast_tree, options, strings, string_value, mode):
    strings = string_function_type_annotations1
    string_value = '"GenericType[int, str]"'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    options = options()
    mode = mode()
    'Ensures that type annotations do not raise violations.'
    tree = parse_ast_tree(mode(strings.format(string_value)))
    option_values = options(max_string_usages=0)
    visitor = StringOveruseVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('string_value', ['"\\t"', '"\\n"', '""'])
@pytest.mark.parametrize('prefix', ['b', 'u', ''])
def test_string_overuse_exceptions(assert_errors, parse_ast_tree, default_options, prefix, string_value):
    string_value = '"\\t"'
    prefix = 'b'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Ensures that over-used strings raise violations.'
    snippet = string_actions.format(prefix + string_value)
    tree = parse_ast_tree(snippet)
    visitor = StringOveruseVisitor(default_options, tree=tree)
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