import pytest
from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.violations.naming import UnusedVariableIsUsedViolation
from wemake_python_styleguide.visitors.ast.functions import FunctionDefinitionVisitor
correct_module = '\n_PROTECTED = 1\nPUBLIC = _PROTECTED + 1\n'
correct_class = '\nclass Test(object):\n    _constant = 1\n\n    def __init__(self):\n        self._protected = 1\n        self.public = self._protected + 1\n\n    def _protected_method(self):\n        ...\n'
correct_function = '\ndef _some_function():\n    first, _second, _ = some_tuple()\n    print(first)\n'
correct_function_with_for = '\ndef some_function():\n    for name, _phone in people.items():\n        print(name)\n'
correct_function_with_exception = '\ndef some_function():\n    try:\n        ...\n    except Exception as exc:\n        print(exc)\n'
correct_function_with_unnamed_exception = '\ndef some_function():\n    try:\n        ...\n    except Exception:\n        ...\n'
correct_func_with_re_store_unused_variable1 = '\ndef logo_and_user():\n    user, _ = some_tuple()\n    logo, _ = some_tuple()\n'
correct_func_with_re_store_unused_variable2 = '\ndef logo_and_user():\n    user, __ = some_tuple()\n    logo, __ = some_tuple()\n'
wrong_function1 = '\ndef some_function():\n    _some = calling()\n    print(_some)\n'
wrong_function2 = '\ndef some_function():\n    first, _some = calling()\n    print(_some)\n'
wrong_function_with_exception = '\ndef some_function():\n    try:\n        ...\n    except Exception as _exc:\n        print(_exc)\n'
wrong_function_with_with = '\ndef some_function():\n    with some() as _ex:\n        print(_ex)\n'
wrong_function_with_for = '\ndef some_function():\n    for _key_item in some():\n        print(_key_item)\n'
wrong_method = '\nclass Test(object):\n    def some_method(self):\n        _some = calling()\n        print(_some)\n'
wrong_function_with_walrus = '\ndef some_function():\n    if _unused := some():\n        print(_unused)\n'

@pytest.mark.parametrize('code', [correct_module, correct_class, correct_function, correct_function_with_for, correct_function_with_exception, correct_function_with_unnamed_exception, correct_func_with_re_store_unused_variable1, correct_func_with_re_store_unused_variable2])
def test_correct_variables(assert_errors, parse_ast_tree, default_options, code, mode):
    code = correct_module
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that correct usage of variables is allowed.'
    tree = parse_ast_tree(mode(code))
    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [wrong_function1, wrong_function2, wrong_function_with_exception, wrong_function_with_with, wrong_function_with_for, wrong_method, pytest.param(wrong_function_with_walrus, marks=pytest.mark.skipif(not PY38, reason='walrus appeared in 3.8'))])
def test_wrong_super_call(assert_errors, parse_ast_tree, code, default_options, mode):
    code = wrong_function1
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that naming and using variables have limitations.'
    tree = parse_ast_tree(mode(code))
    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UnusedVariableIsUsedViolation])

def test_double_wrong_variables(assert_errors, parse_ast_tree, default_options, mode):
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that it is possible to have two violations with wrong vars.'
    code = '\n    def some_function():\n        _should_not_be_used = 1\n        print(_should_not_be_used)\n        print(_should_not_be_used)\n    '
    tree = parse_ast_tree(mode(code))
    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [UnusedVariableIsUsedViolation, UnusedVariableIsUsedViolation])
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