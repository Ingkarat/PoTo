import pytest
from wemake_python_styleguide.violations.best_practices import GetterWithoutReturnViolation
from wemake_python_styleguide.visitors.ast.functions import FunctionSignatureVisitor
getter_function_with_implicit_return = "\ndef get_foo():\n    print('Hello world!')\n"
getter_function_with_bare_return = '\ndef get_foo():\n    return\n'
getter_function_with_valued_return = '\ndef get_foo():\n    return 1\n'
getter_function_with_explicit_none_return = '\ndef get_foo():\n    return None\n'
getter_function_with_bare_yield = '\ndef get_foo():\n    yield\n'
getter_function_with_valued_yield = '\ndef get_foo():\n    yield 1\n'
getter_function_with_explicit_none_yield = '\ndef get_foo():\n    yield None\n'
getter_function_with_yield_from = '\ndef get_foo():\n    yield from [1]\n'
getter_method_with_implicit_return = "\nclass Foo:\n    def get_foo(self):\n        print('Hello world')\n"
getter_method_with_bare_return = '\nclass Foo:\n    def get_foo(self):\n        return\n'
getter_method_with_valued_return = '\nclass Foo:\n    def get_foo(self):\n        return 1\n'
getter_method_with_explicit_none_return = '\nclass Foo:\n    def get_foo(self):\n        return None\n'
getter_method_with_bare_yield = '\nclass Foo:\n    def get_foo(self):\n        yield\n'
getter_method_with_valued_yield = '\nclass Foo:\n    def get_foo(self):\n        yield 1\n'
getter_method_with_explicit_none_yield = '\nclass Foo:\n    def get_foo(self):\n        yield None\n'
getter_method_with_yield_from = '\nclass Foo:\n    def get_foo(self):\n        yield from [1]\n'
regular_function_with_bare_return = '\nclass Foo:\n    def foo(self):\n        return\n'
regular_function_with_implicit_return = "\nclass Foo:\n    def foo(self):\n        print('Hello World!')\n"
regular_function_with_bare_return = '\nclass Foo:\n    def foo(self):\n        return\n'
regular_function_with_bare_yield = '\nclass Foo:\n    def foo(self):\n        yield\n'
regular_method_with_bare_return = '\nclass Foo:\n    def foo(self):\n        return\n'
regular_method_with_implicit_return = "\nclass Foo:\n    def foo(self):\n        print('Hello world')\n"
regular_method_with_bare_return = '\nclass Foo:\n    def foo(self):\n        return\n'
regular_method_with_bare_yield = '\nclass Foo:\n    def foo(self):\n        yield\n'
getter_method_with_branched_return = '\ndef get_foo():\n    if bar:\n        return 1\n'
getter_stub_with_docstring = "\ndef get_foo():\n    '''Gets foo.'''\n"
getter_stub_with_ellipsis = '\ndef get_foo():\n    ...\n'
getter_stub_with_raise = "\ndef get_foo():\n    raise ValueError('Error')\n"
getter_stub_with_docstring_and_ellipsis = "\ndef get_foo():\n    '''Gets foo.'''\n    ...\n"
getter_stub_with_docstring_and_raise = "\ndef get_foo():\n    '''Gets Foo.'''\n    raise ValueError('Error')\n"
getter_stub_with_extra_statements = "\ndef get_foo():\n    '''Gets foo.'''\n    print('Hello World')\n    ...\n"

@pytest.mark.parametrize('code', [getter_function_with_implicit_return, getter_function_with_bare_return, getter_method_with_implicit_return, getter_method_with_bare_return, getter_stub_with_extra_statements])
def test_wrong_getters(assert_errors, parse_ast_tree, default_options, code, mode):
    code = getter_function_with_implicit_return
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that getters which do not output values are forbidden.'
    tree = parse_ast_tree(mode(code))
    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [GetterWithoutReturnViolation])

@pytest.mark.parametrize('code', [getter_function_with_valued_return, getter_function_with_explicit_none_return, getter_function_with_bare_yield, getter_function_with_valued_yield, getter_function_with_explicit_none_yield, getter_method_with_valued_return, getter_method_with_explicit_none_return, getter_method_with_bare_yield, getter_method_with_valued_yield, getter_method_with_explicit_none_yield, getter_method_with_branched_return, getter_stub_with_docstring, getter_stub_with_ellipsis, getter_stub_with_raise, getter_stub_with_docstring_and_ellipsis, getter_stub_with_docstring_and_raise])
def test_correct_getters(assert_errors, parse_ast_tree, default_options, code, mode):
    code = getter_function_with_valued_return
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that getters which output values are allowed.'
    tree = parse_ast_tree(mode(code))
    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [getter_function_with_yield_from, getter_method_with_yield_from])
def test_correct_getter_with_yield_from(assert_errors, parse_ast_tree, default_options, code):
    code = getter_function_with_yield_from
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    '\n    Testing that getters with ``yield from`` expressions are allowed.\n\n    They need to be tested separately because ``yield from`` cannot be\n    used in ``async`` functions.\n    '
    tree = parse_ast_tree(code)
    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [regular_function_with_bare_return, regular_function_with_implicit_return, regular_function_with_bare_yield, regular_method_with_bare_return, regular_method_with_implicit_return, regular_method_with_bare_yield])
def test_correct_non_getters(assert_errors, parse_ast_tree, default_options, code, mode):
    code = regular_function_with_bare_return
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that non-getter functions are allowed to not output values.'
    tree = parse_ast_tree(mode(code))
    visitor = FunctionSignatureVisitor(default_options, tree=tree)
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