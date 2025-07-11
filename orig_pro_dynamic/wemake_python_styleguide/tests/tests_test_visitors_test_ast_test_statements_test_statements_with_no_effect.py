import pytest
from wemake_python_styleguide.violations.best_practices import StatementHasNoEffectViolation
from wemake_python_styleguide.violations.refactoring import MisrefactoredAssignmentViolation
from wemake_python_styleguide.visitors.ast.statements import StatementsWithBodiesVisitor
module_template = '\n{0}\n'
if_template = '\nif some:\n    {0}\n'
if_elif_template = '\nif some:\n    print()\nelif not some:\n    {0}\n'
if_else_template = '\nif some:\n    print()\nelse:\n    {0}\n'
for_template = '\nfor some in []:\n    {0}\n'
for_else_template = '\nfor some in []:\n    print()\nelse:\n    {0}\n'
while_template = '\nwhile True:\n    {0}\n'
while_else_template = '\nwhile True:\n    print()\nelse:\n    {0}\n'
try_template = '\ntry:\n    {0}\nexcept Exception:\n    print()\n'
try_except_template = '\ntry:\n    print()\nexcept Exception:\n    {0}\n'
try_else_template = '\ntry:\n    print()\nexcept Exception:\n    print()\nelse:\n    {0}\n'
try_finally_template = '\ntry:\n    print()\nfinally:\n    {0}\n'
with_template = '\nwith some:\n    {0}\n'
function_template = '\ndef function():\n    {0}\n'
class_template = '\nclass Test(object):\n    {0}\n'
async_function_template = '\nasync def function():\n    {0}\n'
async_with_template = '\nasync def container():\n    async with some:\n        {0}\n'
async_for_template = '\nasync def container():\n    async for some in []:\n        {0}\n'
async_for_else_template = '\nasync def container():\n    async for some in []:\n        print()\n    else:\n        {0}\n'

@pytest.mark.parametrize('code', [module_template, if_template, if_elif_template, if_else_template, for_template, for_else_template, while_template, while_else_template, try_template, try_except_template, try_else_template, try_finally_template, with_template, function_template, class_template, async_function_template, async_with_template, async_for_template, async_for_else_template])
@pytest.mark.parametrize('statement', ['print', 'object.mro', '3 > 4', '1 + 2', '-100'])
def test_statement_with_no_effect(assert_errors, parse_ast_tree, code, statement, default_options):
    code = module_template
    statement = 'print'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that unreachable code is detected.'
    tree = parse_ast_tree(code.format(statement))
    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [StatementHasNoEffectViolation])

@pytest.mark.parametrize('code', [module_template])
@pytest.mark.parametrize('statement', ['x += x + 2', 'x -= x - 1', 'x *= x * 1', 'x /= x / 1', 'x **= x ** 1', 'x ^= x ^ 1', 'x %= x % 1', 'x >>= x >> 1', 'x <<= x << 1', 'x &= x & 1', 'x |= x | 1'])
def test_misrefactored_assignment(assert_errors, parse_ast_tree, code, statement, default_options):
    code = module_template
    statement = 'x += x + 2'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that unreachable code is detected.'
    tree = parse_ast_tree(code.format(statement))
    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [MisrefactoredAssignmentViolation])

@pytest.mark.parametrize('code', [module_template, if_template, if_elif_template, if_else_template, for_template, for_else_template, while_template, while_else_template, try_template, try_except_template, try_else_template, try_finally_template, with_template, function_template, class_template, async_function_template, async_with_template, async_for_template, async_for_else_template])
@pytest.mark.parametrize('statement', ['some_name = 1 + 2', 'call()', 'object.mro()', 'del some', 'some_var: int', 'x += 2', 'x += y + 2', 'x += check(2)', 'x -= 1', 'x *= 1', 'x **= 1', 'x /= 1', 'x ^= 1', 'x %= 1', 'x >>= 1', 'x <<= 1', 'x &= 1', 'x |= 1', 'x -= x.attr("a")', 'x -= test(x)', 'x -= x.method()', 'x -= x.attr + 1', 'x -= test(x) + 1', 'x = 2 + x'])
def test_statement_with_regular_effect(assert_errors, parse_ast_tree, code, statement, default_options):
    code = module_template
    statement = 'some_name = 1 + 2'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing functions, methods, and assignment works.'
    tree = parse_ast_tree(code.format(statement))
    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [function_template])
@pytest.mark.parametrize('statement', ['return', 'yield', 'yield from some', 'raise TypeError()'])
def test_statement_with_function_effect(assert_errors, parse_ast_tree, code, statement, default_options):
    code = function_template
    statement = 'return'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that `return` and `yield` works.'
    tree = parse_ast_tree(code.format(statement))
    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [async_function_template])
@pytest.mark.parametrize('statement', ['await some', 'return', 'yield', 'raise TypeError()'])
def test_statement_with_await_effect(assert_errors, parse_ast_tree, code, statement, default_options):
    code = async_function_template
    statement = 'await some'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that `await` works.'
    tree = parse_ast_tree(code.format(statement))
    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [function_template, async_function_template, class_template, module_template])
@pytest.mark.parametrize('statement', ['"docstring"'])
def test_statement_with_docstring(assert_errors, parse_ast_tree, code, statement, default_options):
    code = function_template
    statement = '"docstring"'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that docstring works.'
    tree = parse_ast_tree(code.format(statement))
    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [if_template, if_elif_template, if_else_template, for_template, for_else_template, while_template, while_else_template, try_template, try_except_template, try_else_template, try_finally_template, with_template, async_with_template, async_for_template, async_for_else_template])
@pytest.mark.parametrize('statement', ['"docstring"'])
def test_statement_with_useless_docstring(assert_errors, parse_ast_tree, code, statement, default_options):
    code = if_template
    statement = '"docstring"'
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that docstring works.'
    tree = parse_ast_tree(code.format(statement))
    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [StatementHasNoEffectViolation])
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