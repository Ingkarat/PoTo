import pytest
from wemake_python_styleguide.violations.consistency import InconsistentReturnVariableViolation
from wemake_python_styleguide.visitors.ast.keywords import ConsistentReturningVariableVisitor
correct_example1 = '\ndef some_function():\n    return 1\n'
correct_example2 = '\ndef some_function():\n    some_value = 1\n    other_value = 2\n    return some_value + other_value\n'
correct_example3 = '\ndef some_function():\n    some_value = 1\n    name = last_name + some_value\n    return name, some_value\n'
correct_example4 = '\ndef some_function():\n    some_value = 1\n    some_value += 1\n    return some_value\n'
correct_example5 = '\ndef some_function():\n    some_value = []\n    some_value.append(1)\n    return some_value\n'
correct_example6 = '\ndef foo():\n    x, _ = some_tuple\n    return x\n'
correct_example7 = '\ndef foo():\n    x.id += some_tuple\n    return x.id\n'
correct_example8 = '\ndef foo():\n    x[0]: int = s[0]\n    return x[0]\n'
correct_example9 = '\ndef foo():\n    x.attr = 1\n    return x.attr\n'
correct_example10 = '\ndef foo():\n    x.attr = 1\n    print()\n    return x.attr\n'
correct_example11 = '\ndef foo():\n    attr = 1\n    print()\n    return attr\n'
correct_example12 = '\ndef some():\n    if something:\n        return something\n'
correct_example13 = '\ndef some():\n    if something:\n        other = 1\n        return something\n'
correct_example14 = '\ndef some():\n    other = 2\n    if something:\n        other = 1\n    else:\n        return other\n'
correct_example15 = '\ndef some():\n    return some\n'
correct_example16 = '\ndef some():\n    x = 1\n    return\n'
correct_example17 = '\ndef some():\n    x, y = 1\n    return y, x\n'
correct_example18 = '\ndef some():\n    x, y, z = 1, 2, 3\n    return x, y\n'
correct_example19 = '\ndef some():\n    x, y, z = 1, 2, 3\n    return y, z\n'
correct_example20 = '\ndef some():\n    x, y, z = 1, 2, 3\n    return 0, y, z\n'
correct_example21 = '\ndef some():\n    x, y, z = 1, 2, 3\n    return x, y, z, 0\n'
correct_example22 = '\ndef some():\n    x, y, z = some\n    return x(), y, z\n'
correct_example23 = '\ndef some():\n    x, y, z = some\n    return x[0], y, z\n'
wrong_example1 = '\ndef function():\n    some_value = 1\n    return some_value\n'
wrong_example2 = '\ndef some_function():\n    some_value = 1\n\n    return some_value\n'
wrong_example3 = '\ndef some_function():\n    some_value: int = 1\n    return some_value\n'
wrong_example4 = '\ndef foo():\n    function_result = function(*args, **kwargs)\n    return function_result\n'
wrong_example5 = '\ndef report_progress(function):\n    def decorator(*args, **kwargs):\n        function_result = function(*args, **kwargs)\n        return function_result\n    return decorator\n'
wrong_example6 = '\ndef wrong_if():\n    if something:\n        other = 1\n        return other\n'
wrong_example7 = '\ndef wrong_if():\n    if something:\n        ...\n    else:\n        other = 1\n        return other\n'
wrong_example8 = '\ndef wrong_for():\n    for i in something:\n        other = i\n        return other\n'
wrong_example9 = '\ndef wrong_for():\n    for i in something:\n        ...\n    else:\n        other = 0\n        return other\n'
wrong_example10 = '\ndef wrong_while():\n    while something:\n        other = 1\n        return other\n'
wrong_example11 = '\ndef wrong_while():\n    while something:\n        ...\n    else:\n        other = 2\n        return other\n'
wrong_example12 = '\ndef wrong_try():\n    try:\n        other = 1\n        return other\n    except:\n        ...\n'
wrong_example13 = '\ndef wrong_try():\n    try:\n        ...\n    except:\n        other = 1\n        return other\n'
wrong_example14 = '\ndef wrong_try():\n    try:\n        ...\n    except:\n        ...\n    else:\n        other = 1\n        return other\n'
wrong_example15 = '\ndef wrong_try():\n    try:\n        ...\n    finally:\n        other = 1\n        return other\n'
wrong_example16 = '\ndef wrong_try():\n    x, y, z = 1, 2, 3\n    return x, y, z\n'
wrong_example16 = '\ndef wrong_try():\n    x, y, z = 1, 2, 3\n    return x, y, z\n'
double_wrong_example1 = '\ndef some():\n    if something() == 1:\n        some = 1\n        return some\n    else:\n        other = 2\n        return other\n'

@pytest.mark.parametrize('code', [wrong_example1, wrong_example2, wrong_example3, wrong_example4, wrong_example5, wrong_example6, wrong_example7, wrong_example8, wrong_example9, wrong_example10, wrong_example11, wrong_example12, wrong_example13, wrong_example14, wrong_example15])
def test_wrong_return_variable(assert_errors, parse_ast_tree, code, default_options, mode):
    code = wrong_example1
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing incorrect `return` statements.'
    tree = parse_ast_tree(mode(code))
    visitor = ConsistentReturningVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [InconsistentReturnVariableViolation])

@pytest.mark.parametrize('code', [correct_example1, correct_example2, correct_example3, correct_example4, correct_example5, correct_example6, correct_example7, correct_example8, correct_example9, correct_example10, correct_example11, correct_example12, correct_example13, correct_example14, correct_example15, correct_example16, correct_example17, correct_example18, correct_example19, correct_example20, correct_example21, correct_example22, correct_example23])
def test_correct_return_statements(assert_errors, parse_ast_tree, code, default_options, mode):
    code = correct_example1
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing correct `return` statements.'
    tree = parse_ast_tree(mode(code))
    visitor = ConsistentReturningVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

def test_double_wrong_return_variable(assert_errors, parse_ast_tree, default_options, mode):
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing double incorrect `return` statements.'
    tree = parse_ast_tree(mode(double_wrong_example1))
    visitor = ConsistentReturningVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [InconsistentReturnVariableViolation, InconsistentReturnVariableViolation])
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