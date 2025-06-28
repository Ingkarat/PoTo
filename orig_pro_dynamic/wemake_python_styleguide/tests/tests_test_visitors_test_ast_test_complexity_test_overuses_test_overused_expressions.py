import pytest
from wemake_python_styleguide.violations.complexity import OverusedExpressionViolation
from wemake_python_styleguide.visitors.ast.complexity.overuses import ExpressionOveruseVisitor
module_context = '\n{0}\n{1}\n'
function_context1 = '\ndef function():\n    {0}\n    {1}\n'
function_context2 = '\n@decorator\ndef function() -> types.Some[None]:\n    {0}\n    {1}\n'
function_context3 = '\n@decorator()\ndef function(arg: List[int]) -> types.NoneType[None]:\n    {0}\n    {1}\n'
function_context4 = '\n@decorator.attr.nested()\ndef function(arg: List[int]) -> types.NoneType[None]:\n    {0}\n    {1}\n'
class_context1 = '\nclass Context(object):\n    {0}\n    {1}\n'
class_context2 = '\nclass Context(object):\n    first: List[int]\n    second: List[int]\n\n    {0}\n    {1}\n'
class_context3 = '\nclass Context(object):\n    first: List[List[int]]\n    second: List[List[int]]\n\n    {0}\n    {1}\n'
method_context1 = '\nclass Context(object):\n    def method(self):\n        {0}\n        {1}\n'
method_context2 = '\nclass Context(object):\n    @decorator.attr\n    @decorator.attr\n    def method(self):\n        {0}\n        {1}\n'
method_context3 = "\nclass Context(object):\n    @decorator.call('a')\n    @decorator.call('a')\n    def method(self, arg: List[int]) -> type.Any:\n        {0}\n        {1}\n"
method_context4 = "\nclass Context(object):\n    def method1(self, arg1: List[int]) -> type.Any:\n        {0}\n        {0}\n\n    # Two methods have the same signature, that's how we check\n    # for return and arg annotations.\n    def method2(self, arg2: List[int]) -> type.Any:\n        ...\n"
method_context5 = '\nclass Context(object):\n    def method1(self, arg1: "List[int]") -> \'type.Any\':\n        ...\n\n    # Two methods have the same signature, that\'s how we check\n    # for return and arg annotations.\n    def method2(self, arg2: "List[int]") -> \'type.Any\':\n        {0}\n        {0}\n'
violating_expressions = ('assert 1', 'a and b', 'b + a', 'call(1, None)', 'a >= 1', '-item.attr', 'lambda x: x.set', '{a: 1 for a in "123"}', '{"1": a}', '[element, other]', '[x for x in some if cond]', '(1, 2, 3)', '(x.attr for x in other)', '{1, 2, 3}', '{a for a in other}', 'self.method([star])', 'self[1, 2, 3]', 'x: types.List[Set[int]] = call(1, 2, 3)')
ignored_expressions = ('super()', 'self.call(1, 2, 3)', 'cls.__private_attribute()', 'mcs._property()', 'self[start:end]', '[]', '()', '{**keys}', '{*set_items}', '""', '1', 'b"context"', 'list()', 'set()', 'dict()', 'some.prop')

@pytest.mark.parametrize('code', [function_context1, function_context2, function_context3, function_context4, method_context1, method_context2, method_context3, method_context4, method_context5])
@pytest.mark.parametrize('expression', violating_expressions)
def test_func_expression_overuse(assert_errors, parse_ast_tree, options, expression, code, mode):
    code = function_context1
    expression = violating_expressions[0]
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    options = options()
    mode = mode()
    'Ensures that settings for expressions over-use work.'
    tree = parse_ast_tree(mode(code.format(expression, expression)))
    option_values = options(max_function_expressions=1)
    visitor = ExpressionOveruseVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [OverusedExpressionViolation])

@pytest.mark.parametrize('code', [module_context])
@pytest.mark.parametrize('expression', violating_expressions)
def test_module_expression_overuse(assert_errors, parse_ast_tree, options, expression, code):
    code = module_context
    expression = violating_expressions[0]
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    options = options()
    'Ensures that settings for expressions over-use work.'
    tree = parse_ast_tree(code.format(expression, expression))
    option_values = options(max_module_expressions=1)
    visitor = ExpressionOveruseVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [OverusedExpressionViolation])

@pytest.mark.parametrize('code', [class_context1, class_context2, class_context3])
@pytest.mark.parametrize('expression', violating_expressions)
def test_class_expression_use(assert_errors, parse_ast_tree, options, expression, code):
    code = class_context1
    expression = violating_expressions[0]
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    options = options()
    'Ensures that settings for expressions over-use work.'
    tree = parse_ast_tree(code.format(expression, expression))
    option_values = options(max_module_expressions=1, max_function_expressions=1)
    visitor = ExpressionOveruseVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [function_context1, function_context2, function_context3, function_context4, class_context1, class_context2, class_context3, method_context1, method_context2, method_context3, method_context4, method_context5, module_context])
@pytest.mark.parametrize('expression', ignored_expressions)
def test_ignored_expressions(assert_errors, parse_ast_tree, options, expression, code, mode):
    code = function_context1
    expression = ignored_expressions[0]
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    options = options()
    mode = mode()
    'Ensures that ignored expressions does not raise violations.'
    tree = parse_ast_tree(mode(code.format(expression, expression)))
    option_values = options(max_function_expressions=1)
    visitor = ExpressionOveruseVisitor(option_values, tree=tree)
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