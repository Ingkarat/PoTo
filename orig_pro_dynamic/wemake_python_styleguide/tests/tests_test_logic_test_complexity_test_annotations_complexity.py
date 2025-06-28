import pytest
from wemake_python_styleguide.logic.complexity import annotations

@pytest.mark.parametrize(('annotation', 'complexity'), [('str', 1), ('int', 1), ('List', 1), ('List[str]', 2), ('List[int]', 2), ('Dict[str, int]', 2), ('Literal[""]', 2), ('Tuple[()]', 2), ('"This is rainbow in the dark!"', 1), ('Tuple[List[int], Optional[Dict[str, int]]]', 4)])
def test_get_annotation_complexity(parse_ast_tree, annotation: str, complexity: int) -> None:
    (annotation, complexity) = ('str', 1)
    parse_ast_tree = parse_ast_tree()
    'Test get_annotation_complexity function.'
    text = 'def f() -> {annotation}: pass\n'.format(annotation=annotation)
    tree = parse_ast_tree(text)
    node = tree.body[0].returns
    assert annotations.get_annotation_complexity(node) == complexity
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