import pytest
from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.violations.best_practices import OuterScopeShadowingViolation
from wemake_python_styleguide.visitors.ast.blocks import BlockVariableVisitor
correct_for_loop1 = '\nimport ast\n\ndef wrapper():\n    for i, j in ():\n        print(i, j)\n'
correct_for_loop2 = '\nfrom some import other\n\ndef wrapper():\n    for i, j in ():\n        return i, j\n'
correct_for_loop3 = '\nimport other\n\nclass Test():\n    z = 1\n\ndef zz():\n    z = 2\n\ndef wrapper():\n    z = 3\n    for i, j in ():\n        yield i, j, z\n'
correct_for_comprehension = '\ndef test():\n    compare = 0\n\ndef context():\n    compare = 1\n    nodes = [\n        print(compare.left)\n        for compare in node.values\n        if isinstance(compare, ast.Compare)\n    ]\n'
correct_except = '\nimport y\n\ndef context():\n    e = 1\n\ntry:\n    ...\nexcept Exception as e:\n    print(e)\n'
correct_with1 = '\ndef wrapper():\n    with open() as (first, second):\n        print(first, second)\n\nclass Test(object):\n    first: str\n\n    def __init__(self, second):\n        self.first = 1\n        self.second = second\n'
correct_with2 = '\ndef context(first):\n    first = first + 1\n\ndef wrapper():\n    with open() as first:\n        print(first)\n    print(wrapper)\n'
correct_with3 = '\ndef wrapper():\n    with open() as first:\n        print(first)\n    print(wrapper)\n\ndef other():\n    first = 1\n    print(first)\n'
correct_class1 = '\nclass Test(object):\n    first: int\n    second = 2\n    third: int = 3\n\n    def method(self):\n        first = 1\n        second = 2\n        third = 3\n\n    def other(self):\n        method = 1\n'
correct_class2 = '\nclass Test(object):\n    first: int\n    second = 2\n    third: int = 3\n\n    def method(self, first, second, third):\n        self.first = first + 1\n        self.second = second + 2\n        self.third = third + 3\n'
correct_class3 = '\nclass First(object):\n    a = 1\n\nclass Second(First):\n    a = 2\n'
correct_class4 = '\na = 0\n\ndef test():\n    ...\n\nclass First(object):\n    a = 1\n\n    def test(self):\n        ...\n'
correct_walrus = '\nimport some\n\ndef function():\n    if other := some:\n        ...\n'
import_overlap1 = '\nimport ast\n\ndef some():\n    ast = 1\n'
import_overlap2 = '\nimport ast as ast_import\n\ndef some():\n    ast_import = 1\n'
import_overlap3 = '\nfrom system import ast\n\ndef some(ast):\n    ast_import = ast + 1\n'
import_overlap4 = '\nfrom system import ast as ast_import\n\ndef some():\n    ast_import = ast + 1\n'
function_overlap1 = '\ndef test():\n    ...\n\ndef other():\n    test = 1\n'
function_overlap2 = '\ndef test():\n    ...\n\ndef other(test):\n    test1 = test + 1\n'
constant_overlap1 = '\na = 1\n\ndef func(a):\n    ...\n'
constant_overlap2 = '\na = 1\n\ndef func():\n    a = 2\n'
constant_overlap3 = '\na = 1\n\ndef func():\n    for a in some():\n        ...\n'
constant_overlap4 = '\na = 1\n\ndef func():\n    try:\n        ...\n    except ValueError as a:\n        ...\n'
constant_overlap5 = '\na = 1\n\ndef func():\n    with open() as a:\n        ...\n'
constant_overlap6 = '\na = 1\n\ndef func():\n    import a\n'
walrus_overlap = '\nimport some\n\ndef function():\n    if some := other():\n        ...\n'

@pytest.mark.parametrize('code', [correct_for_loop1, correct_for_loop2, correct_for_loop3, correct_for_comprehension, correct_except, correct_with1, correct_with2, correct_with3, correct_class1, correct_class2, correct_class3, correct_class4, pytest.param(correct_walrus, marks=pytest.mark.skipif(not PY38, reason='walrus appeared in 3.8'))])
def test_variable_used_correctly(assert_errors, parse_ast_tree, default_options, code, mode):
    code = correct_for_loop1
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that using variables inside a block is correct.'
    tree = parse_ast_tree(mode(code))
    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [import_overlap1, import_overlap2, import_overlap3, import_overlap4, function_overlap1, function_overlap2, constant_overlap1, constant_overlap2, constant_overlap3, constant_overlap4, constant_overlap5, constant_overlap6, pytest.param(walrus_overlap, marks=pytest.mark.skipif(not PY38, reason='walrus appeared in 3.8'))])
def test_outer_variable_shadow(assert_errors, parse_ast_tree, default_options, code, mode):
    code = import_overlap1
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that shadowing vars are not allowed.'
    tree = parse_ast_tree(mode(code))
    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [OuterScopeShadowingViolation])

def test_outer_variable_double_shadow(assert_errors, parse_ast_tree, default_options, mode):
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    mode = mode()
    'Testing that shadowing vars are not allowed.'
    code = '\n    a = 1\n\n    def test1():\n        a = 2\n\n    def test2(a):\n        ...\n    '
    tree = parse_ast_tree(mode(code))
    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [OuterScopeShadowingViolation, OuterScopeShadowingViolation])
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