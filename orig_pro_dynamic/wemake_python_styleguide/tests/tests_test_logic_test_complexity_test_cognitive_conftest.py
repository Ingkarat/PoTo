"""
Fixtures to make testing cognitive complexity easy.

Policy for testing cognitive complexity:

1. Use a single function def in code samples
2. Write ``# +x`` comments on each line where addition happens

Adapted from https://github.com/Melevir/cognitive_complexity
"""
import ast
import pytest
from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.logic.complexity import cognitive

def _find_function(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, FunctionNodes):
            return node
    return None

@pytest.fixture(scope='session')
def get_code_snippet_complexity(parse_ast_tree):
    parse_ast_tree = parse_ast_tree()
    'Fixture to parse and count cognitive complexity the easy way.'

    def factory(src: str) -> int:
        funcdef = _find_function(parse_ast_tree(src))
        assert funcdef, 'No function definition found'
        return cognitive.cognitive_score(funcdef)
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