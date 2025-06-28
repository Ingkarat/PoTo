import pytest
from wemake_python_styleguide.options.defaults import NESTED_CLASSES_WHITELIST
from wemake_python_styleguide.violations.best_practices import NestedClassViolation
from wemake_python_styleguide.visitors.ast.complexity.nested import NestedComplexityVisitor
nested_class_in_class = '\nclass Parent(object):\n    class {0}(object): ...\n'
nested_class_in_method = '\nclass Parent(object):\n    def container(self):\n        class {0}(object): ...\n'
nested_class_in_function = '\ndef container():\n    class {0}(object): ...\n'
nested_class_in_if = '\ndef container():\n    if some_value:\n        class {0}(object): ...\n'
nested_class_in_if_else = '\ndef container():\n    if some_value:\n        ...\n    else:\n        class {0}(object): ...\n'
nested_class_in_context_manager = '\ndef container():\n    with open() as file_obj:\n        class {0}(object): ...\n'
nested_class_in_for_loop = '\ndef container():\n    for some in iterable():\n        class {0}(object): ...\n'
nested_class_in_while_loop = '\ndef container():\n    while True:\n        class {0}(object): ...\n'
nested_class_in_try = '\ndef container():\n    try:\n        class {0}(object): ...\n    except:\n        ...\n'
nested_class_in_except = '\ndef container():\n    try:\n        ...\n    except:\n        class {0}(object): ...\n'
nested_class_in_try_else = '\ndef container():\n    try:\n        ...\n    except:\n        ...\n    else:\n        class {0}(object): ...\n'
nested_class_in_try_finally = '\ndef container():\n    try:\n        ...\n    finally:\n        class {0}(object): ...\n'

@pytest.mark.parametrize('code', [nested_class_in_class, nested_class_in_method, nested_class_in_function, nested_class_in_if, nested_class_in_if_else, nested_class_in_context_manager, nested_class_in_for_loop, nested_class_in_while_loop, nested_class_in_try, nested_class_in_except, nested_class_in_try_else, nested_class_in_try_finally])
def test_nested_class(assert_errors, assert_error_text, parse_ast_tree, code, default_options, mode):
    code = nested_class_in_class
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that nested classes are restricted.'
    nested_name = 'NestedClass'
    tree = parse_ast_tree(mode(code.format(nested_name)))
    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [NestedClassViolation])
    assert_error_text(visitor, nested_name)

@pytest.mark.parametrize('whitelist_name', NESTED_CLASSES_WHITELIST)
@pytest.mark.parametrize('code', [nested_class_in_class])
def test_whitelist_nested_classes(assert_errors, parse_ast_tree, whitelist_name, code, default_options, mode):
    whitelist_name = NESTED_CLASSES_WHITELIST[0]
    code = nested_class_in_class
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that it is possible to nest whitelisted classes.'
    tree = parse_ast_tree(mode(code.format(whitelist_name)))
    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('whitelist_name', [*NESTED_CLASSES_WHITELIST, 'NestedClass'])
@pytest.mark.parametrize('code', [nested_class_in_class])
def test_custom_whitelist_nested_classes(assert_errors, parse_ast_tree, whitelist_name, code, options, mode):
    whitelist_name = *NESTED_CLASSES_WHITELIST
    code = nested_class_in_class
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    options = options()
    mode = mode()
    'Testing that it is possible to nest custom whitelisted classes.'
    tree = parse_ast_tree(mode(code.format(whitelist_name)))
    option_values = options(nested_classes_whitelist=[*NESTED_CLASSES_WHITELIST, 'NestedClass'])
    visitor = NestedComplexityVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('whitelist_name', [*NESTED_CLASSES_WHITELIST, 'NestedClass'])
@pytest.mark.parametrize('code', [nested_class_in_method, nested_class_in_function, nested_class_in_if, nested_class_in_if_else, nested_class_in_context_manager, nested_class_in_for_loop, nested_class_in_while_loop, nested_class_in_try, nested_class_in_except, nested_class_in_try_else, nested_class_in_try_finally])
def test_whitelist_nested_classes_in_functions(assert_errors, assert_error_text, parse_ast_tree, whitelist_name, code, default_options, mode):
    whitelist_name = *NESTED_CLASSES_WHITELIST
    code = nested_class_in_method
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that it is restricted to nest any classes in functions.'
    tree = parse_ast_tree(mode(code.format(whitelist_name)))
    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [NestedClassViolation])
    assert_error_text(visitor, whitelist_name)

def test_ordinary_class(assert_errors, parse_ast_tree, default_options, mode):
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that it is possible to write basic classes.'
    code = '\n    class Ordinary(object):\n        def method(self): ...\n\n    class Second(Ordinary):\n        def method(self): ...\n    '
    tree = parse_ast_tree(mode(code))
    visitor = NestedComplexityVisitor(default_options, tree=tree)
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