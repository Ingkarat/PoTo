import pytest
from wemake_python_styleguide.violations.oop import WrongSuperCallAccessViolation, WrongSuperCallViolation
from wemake_python_styleguide.visitors.ast.functions import WrongFunctionCallVisitor
super_call_with_access = '\nclass Example(Parent):\n    def some_thing(self):\n        super({0}).{1}\n'
correct_super_call = '\nclass Example(object):\n    def some_method(self, arg1):\n        super().some_method(arg1)\n'
correct_regression520 = '\nclass Test:\n    def __init__(self):\n        super().__init__()\n\n\ndef another():\n    def func():\n        return 1\n\n    return func\n'
super_call_in_module = '\nsuper()\n'
super_call_in_module_with_arguments = '\nsuper(SomeClass, instance)\n'
super_call_in_function = '\ndef some_function():\n    super()\n'
super_call_in_function_with_arguments = '\ndef some_function():\n    super(SomeClass, instance)\n'
super_call_in_method_with_arguments = '\nclass Example(object):\n    def some_method(self, arg1):\n        super(Example, self).some_method(arg1)\n'

@pytest.mark.parametrize('code', [correct_super_call, correct_regression520])
def test_correct_super_call(assert_errors, parse_ast_tree, default_options, code, mode):
    code = correct_super_call
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that calling `super` in method is fine.'
    tree = parse_ast_tree(mode(code))
    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [super_call_in_module, super_call_in_function, super_call_in_method_with_arguments])
def test_wrong_super_call(assert_errors, parse_ast_tree, code, default_options, mode):
    code = super_call_in_module
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that calling `super` has limitations.'
    tree = parse_ast_tree(mode(code))
    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [WrongSuperCallViolation])

@pytest.mark.parametrize('code', [super_call_in_function_with_arguments, super_call_in_module_with_arguments])
def test_double_wrong_super_call(assert_errors, parse_ast_tree, code, default_options, mode):
    code = super_call_in_function_with_arguments
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that it is possible to have two violations with `super`.'
    tree = parse_ast_tree(mode(code))
    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [WrongSuperCallViolation, WrongSuperCallViolation])

@pytest.mark.parametrize('code', [super_call_with_access])
@pytest.mark.parametrize(('arg', 'prop'), [('', 'other()'), ('', 'other'), ('', 'other.nested'), ('', 'other.method()'), ('', 'other["key"]')])
def test_wrong_access_super_call_with_no_args(assert_errors, parse_ast_tree, code, arg, prop, default_options, mode):
    code = super_call_with_access
    (arg, prop) = ('', 'other()')
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that calling `super` with incorrect access is restricted.'
    tree = parse_ast_tree(mode(code.format(arg, prop)))
    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [WrongSuperCallAccessViolation])

@pytest.mark.parametrize('code', [super_call_with_access])
@pytest.mark.parametrize(('arg', 'prop'), [('Class, self', 'other()'), ('Class, self', 'other'), ('Class, self', 'other.nested'), ('Class, self', 'other.method()'), ('Class, self', 'other["key"]')])
def test_wrong_access_super_call_with_args(assert_errors, parse_ast_tree, code, arg, prop, default_options, mode):
    code = super_call_with_access
    (arg, prop) = ('Class, self', 'other()')
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that calling `super` with incorrect access is restricted.'
    tree = parse_ast_tree(mode(code.format(arg, prop)))
    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [WrongSuperCallAccessViolation, WrongSuperCallViolation])
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