from typing import List, NamedTuple
import pytest
from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.violations import oop
from wemake_python_styleguide.visitors.ast.classes import WrongMethodVisitor
regular_method_detailed = '\nclass Useless(object):\n    {decorator}\n    def function(self, {args_definition}):\n        {statements}\n        super({super_args}).{method_name}({args_invocation})\n'
regular_method_detailed_with_return = '\nclass Useless(object):\n    {decorator}\n    def function(self, {args_definition}):\n        {statements}\n        return super({super_args}).{method_name}({args_invocation})\n'
regular_method_short = '\nclass Useless(object):\n    def function({args}):\n        {statement}\n'
regular_method_short_with_extra = '\nclass Useless(object):\n    def function({args}):\n        {statement}\n        return None\n'
_MethodArgs = NamedTuple('_MethodArgs', definition=str, invocation=str)
valid_method_args: List[_MethodArgs] = [_MethodArgs('', ''), _MethodArgs('a', 'a'), _MethodArgs('a, b', 'a, b'), _MethodArgs('a, *, b', 'a, b=b'), _MethodArgs('*, a, b', 'a=a, b=b'), _MethodArgs('*, a, b', 'b=b, a=a'), _MethodArgs('a, *args', 'a, *args'), _MethodArgs('a, *args, **kwargs', 'a, *args, **kwargs'), _MethodArgs('*, a, **kwargs', 'a=a, **kwargs'), _MethodArgs('*, a, **kwargs', '**kwargs, a=a')]
if PY38:
    valid_method_args.extend([_MethodArgs('/, a, b', 'a, b'), _MethodArgs('a, /, b', 'a, b'), _MethodArgs('a, b, /', 'a, b'), _MethodArgs('a, /, b, *, c', 'a, b, c=c'), _MethodArgs('a, /, b, *args, **kwargs', 'a, b, *args, **kwargs'), _MethodArgs('a, /, b, *arg, c, **kw', 'a, b, *arg, **kw, c=c')])
valid_statements = ['"""Valid docstring."""', '']
valid_super_args = ('', 'Useless, self', 'Useless, obj=self', 't=Useless, obj=self', 'obj=self, t=Useless')
invalid_method_args: List[_MethodArgs] = [_MethodArgs('', 'a=1'), _MethodArgs('', '1'), _MethodArgs('a', ''), _MethodArgs('a', 'a, 1'), _MethodArgs('a, b', 'a'), _MethodArgs('a, b', 'a, b, 1'), _MethodArgs('a, b', 'a, b=1'), _MethodArgs('a, *, b', 'a'), _MethodArgs('a, *, b', '1, b'), _MethodArgs('a, *, b', 'a, b=1'), _MethodArgs('a, *, b', 'a=1, b=b'), _MethodArgs('a, *, b', 'a, b=b, c=1'), _MethodArgs('*, a, b', 'a=a, b=1'), _MethodArgs('*, a, b', 'b=b, a=1'), _MethodArgs('a, *args', 'a'), _MethodArgs('a, *args', 'a, 1, *args'), _MethodArgs('a, *args', 'a=1, *args'), _MethodArgs('a, *args, **kwargs', 'a'), _MethodArgs('a, *args, **kwargs', 'a, *args'), _MethodArgs('a, *args, **kwargs', 'a, *args, **kwargs2'), _MethodArgs('a, *args, **kwargs', 'a, *args2, **kwargs'), _MethodArgs('a, *args, **kwargs', 'a, 1, *args, **kwargs'), _MethodArgs('a, *args, **kwargs', '1, *args, **kwargs'), _MethodArgs('a, *args, **kwargs', 'a, *args, b=1, **kwargs'), _MethodArgs('a, *args, **kwargs', 'a=1, *args, **kwargs'), _MethodArgs('*, a, **kwargs', 'a=a'), _MethodArgs('*, a, **kwargs', '**kwargs'), _MethodArgs('*, a, **kwargs', 'a=a, b=1, **kwargs')]
invalid_statements = ['print(1)', 'a = 1', 'self.other()', '"""Docstring."""; print(1)']
invalid_super_args = ('Useless', 'Useless, object', 'Useless(), self', 'Useless, obj=object', 't=Useless, obj=object', 't=Useless(), obj=self', 'Useless(), obj=self', 't=Useless, obj=self, unknown=1', 't=Useless, incorrect=self')

@pytest.mark.parametrize('code', [regular_method_detailed, regular_method_detailed_with_return])
@pytest.mark.parametrize('statements', valid_statements)
@pytest.mark.parametrize('method_args', valid_method_args)
@pytest.mark.parametrize('super_args', valid_super_args)
def test_useless_overwriting(assert_errors, parse_ast_tree, mode, code, statements, super_args, method_args, default_options):
    code = regular_method_detailed
    statements = valid_statements[0]
    method_args = valid_method_args[0]
    super_args = valid_super_args[0]
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    mode = mode()
    default_options = default_options()
    'Testing situations with useless overwriting.'
    formatted_code = mode(code.format(decorator='', args_definition=method_args.definition, statements=statements, super_args=super_args, method_name='function', args_invocation=method_args.invocation))
    tree = parse_ast_tree(formatted_code)
    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [oop.UselessOverwrittenMethodViolation])

@pytest.mark.parametrize('code', [regular_method_detailed, regular_method_detailed_with_return])
@pytest.mark.parametrize('decorator', ['@decorator'])
@pytest.mark.parametrize('statements', valid_statements)
@pytest.mark.parametrize('method_args', valid_method_args)
@pytest.mark.parametrize('super_args', valid_super_args)
def test_useful_due_to_invalid_decorator(assert_errors, parse_ast_tree, mode, decorator, code, statements, super_args, method_args, default_options):
    code = regular_method_detailed
    decorator = '@decorator'
    statements = valid_statements[0]
    method_args = valid_method_args[0]
    super_args = valid_super_args[0]
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    mode = mode()
    default_options = default_options()
    'Testing situations with useful overwriting due to invalid decorator.'
    formatted_code = mode(code.format(decorator=decorator, args_definition=method_args.definition, statements=statements, super_args=super_args, method_name='function', args_invocation=method_args.invocation))
    tree = parse_ast_tree(formatted_code)
    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [regular_method_detailed, regular_method_detailed_with_return])
@pytest.mark.parametrize('statements', invalid_statements)
@pytest.mark.parametrize('method_args', valid_method_args)
@pytest.mark.parametrize('super_args', valid_super_args)
def test_useful_due_to_invalid_statements(assert_errors, parse_ast_tree, mode, code, statements, super_args, method_args, default_options):
    code = regular_method_detailed
    statements = invalid_statements[0]
    method_args = valid_method_args[0]
    super_args = valid_super_args[0]
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    mode = mode()
    default_options = default_options()
    'Testing situations with useful overwriting due to invalid statements.'
    formatted_code = mode(code.format(decorator='', args_definition=method_args.definition, statements=statements, super_args=super_args, method_name='function', args_invocation=method_args.invocation))
    tree = parse_ast_tree(formatted_code)
    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [regular_method_detailed, regular_method_detailed_with_return])
@pytest.mark.parametrize('statements', valid_statements)
@pytest.mark.parametrize('method_args', valid_method_args)
@pytest.mark.parametrize('super_args', invalid_super_args)
def test_useful_due_to_invalid_super_args(assert_errors, parse_ast_tree, mode, code, statements, super_args, method_args, default_options):
    code = regular_method_detailed
    statements = valid_statements[0]
    method_args = valid_method_args[0]
    super_args = invalid_super_args[0]
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    mode = mode()
    default_options = default_options()
    'Testing situations with useful overwriting due to invalid super args.'
    formatted_code = mode(code.format(decorator='', args_definition=method_args.definition, statements=statements, super_args=super_args, method_name='function', args_invocation=method_args.invocation))
    tree = parse_ast_tree(formatted_code)
    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [regular_method_detailed, regular_method_detailed_with_return])
@pytest.mark.parametrize('statements', valid_statements)
@pytest.mark.parametrize('method_args', valid_method_args)
@pytest.mark.parametrize('super_args', valid_super_args)
def test_useful_due_to_invalid_method(assert_errors, parse_ast_tree, mode, code, statements, super_args, method_args, default_options):
    code = regular_method_detailed
    statements = valid_statements[0]
    method_args = valid_method_args[0]
    super_args = valid_super_args[0]
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    mode = mode()
    default_options = default_options()
    'Testing situations with useful overwriting due to invalid method.'
    formatted_code = mode(code.format(decorator='', args_definition=method_args.definition, statements=statements, super_args=super_args, method_name='invalid_function', args_invocation=method_args.invocation))
    tree = parse_ast_tree(formatted_code)
    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [regular_method_detailed, regular_method_detailed_with_return])
@pytest.mark.parametrize('statements', valid_statements)
@pytest.mark.parametrize('method_args', invalid_method_args)
@pytest.mark.parametrize('super_args', valid_super_args)
def test_useful_due_to_invalid_method_args(assert_errors, parse_ast_tree, mode, code, statements, super_args, method_args, default_options):
    code = regular_method_detailed
    statements = valid_statements[0]
    method_args = invalid_method_args[0]
    super_args = valid_super_args[0]
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    mode = mode()
    default_options = default_options()
    'Testing situations with useful overwriting due to invalid method args.'
    formatted_code = mode(code.format(decorator='', args_definition=method_args.definition, statements=statements, super_args=super_args, method_name='function', args_invocation=method_args.invocation))
    tree = parse_ast_tree(formatted_code)
    visitor = WrongMethodVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [regular_method_short, regular_method_short_with_extra])
@pytest.mark.parametrize(('args', 'statement'), [('self', '""""""'), ('self', 'return 1'), ('self', 'return Useless.function()'), ('self', 'return Useless().function()'), ('self', 'return Useless()().function()'), ('this', 'return super().function()')])
def test_useful_due_to_incorrect_main_statement(assert_errors, parse_ast_tree, mode, code, args, statement, default_options):
    code = regular_method_short
    (args, statement) = ('self', '""""""')
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    mode = mode()
    default_options = default_options()
    'Testing useful overwriting due to totally different body.'
    formatted_code = mode(code.format(args=args, statement=statement))
    tree = parse_ast_tree(formatted_code)
    visitor = WrongMethodVisitor(default_options, tree=tree)
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