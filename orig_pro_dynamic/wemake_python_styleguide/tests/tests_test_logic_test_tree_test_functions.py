import pytest
from wemake_python_styleguide.logic.tree import functions

@pytest.mark.parametrize(('function_call', 'function_name'), [('print("Hello world!")', 'print'), ('int("10")', 'int'), ('bool(1)', 'bool'), ('open("/tmp/file.txt", "r")', 'open'), ('str(10)', 'str'), ('datetime.timedelta(days=1)', 'datetime.timedelta'), ('cmath.sqrt(100)', 'cmath.sqrt'), ('dt.strftime("%H:%M")', 'dt.strftime'), ('obj.funct()', 'obj.funct')])
def test_given_function_called_no_split(parse_ast_tree, function_call: str, function_name: str) -> None:
    (function_call, function_name) = ('print("Hello world!")', 'print')
    parse_ast_tree = parse_ast_tree()
    'Test given_function_called without splitting the modules.'
    tree = parse_ast_tree(function_call)
    node = tree.body[0].value
    called_function = functions.given_function_called(node, [function_name])
    assert called_function == function_name

@pytest.mark.parametrize(('function_call', 'function_name'), [('print("Hello world!")', 'print'), ('int("10")', 'int'), ('bool(1)', 'bool'), ('open("/tmp/file.txt", "r")', 'open'), ('str(10)', 'str'), ('datetime.timedelta(days=1)', 'timedelta'), ('cmath.sqrt(100)', 'sqrt'), ('dt.strftime("%H:%M")', 'strftime'), ('obj.funct()', 'funct')])
def test_given_function_called_with_split(parse_ast_tree, function_call: str, function_name: str) -> None:
    (function_call, function_name) = ('print("Hello world!")', 'print')
    parse_ast_tree = parse_ast_tree()
    'Test given_function_called splitting the modules.'
    tree = parse_ast_tree(function_call)
    node = tree.body[0].value
    called_function = functions.given_function_called(node, [function_name], split_modules=True)
    assert called_function == function_name
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