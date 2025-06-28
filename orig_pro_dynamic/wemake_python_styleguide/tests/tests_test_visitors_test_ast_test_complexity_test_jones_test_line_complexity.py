import pytest
from wemake_python_styleguide.violations.complexity import LineComplexityViolation
from wemake_python_styleguide.visitors.ast.complexity.jones import JonesComplexityVisitor
line_simple = 'x = 2'
line_with_types = 'x: int = 2'
line_with_complex_types = 'x: Dict[Tuple[str, str, int], Set[List[attr.Val]]]'
line_with_comprehension = 'x = [f for f in "abc"]'
line_with_math = 'x = y * 2 + 19 / 9.3'
line_inside_function = '\ndef some_function():\n    return 2 + 1\n'
line_inside_async_function = '\nasync def some_function():\n    return 2 + 1\n'
line_inside_class = '\nclass SomeClass(object):\n    field = 13 / 2\n'
class_with_function = '\nclass First(object):\n    def second():\n        return 2 + 1\n'
class_with_async_function = '\nclass First(object):\n    async def second():\n        return 2 + 1\n'
class_with_usual_and_async_function = '\nclass First(object):\n    async def second():\n        return 2 + 1\n\n    def third():\n        return 2 + 2\n'
function_declaration = 'def some_function(): ...'
async_function_declaration = 'async def some_function(): ...'
class_declaration = 'class SomeClass(object): ...'
empty_module = ''
regression1216 = 'call.endswith(post) and len(node.args) == self._post[post]'

@pytest.mark.parametrize('code', [line_simple, line_with_types, line_with_complex_types, line_with_comprehension, line_with_math, line_inside_function, line_inside_async_function, line_inside_class, function_declaration, async_function_declaration, class_declaration, empty_module, class_with_function, class_with_async_function, class_with_usual_and_async_function])
def test_regular_nodes(assert_errors, parse_ast_tree, code, default_options):
    code = line_simple
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that regular nodes do not raise violations.'
    tree = parse_ast_tree(code)
    visitor = JonesComplexityVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize(('code', 'complexity'), [(line_simple, 3), (line_with_types, 3), (line_with_complex_types, 2), (line_with_comprehension, 6), (line_with_math, 9), (line_inside_function, 4), (line_inside_async_function, 4), (line_inside_class, 5), (class_with_function, 4), (class_with_async_function, 4)])
def test_complex_lines(assert_errors, assert_error_text, parse_ast_tree, code, complexity, options):
    (code, complexity) = (line_simple, 3)
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    parse_ast_tree = parse_ast_tree()
    options = options()
    'Testing that complex lines do raise violations.'
    tree = parse_ast_tree(code)
    option_values = options(max_line_complexity=1)
    visitor = JonesComplexityVisitor(option_values, tree=tree)
    visitor.run()
    assert_errors(visitor, [LineComplexityViolation])
    assert_error_text(visitor, str(complexity), option_values.max_line_complexity)

def test_same_complexity(parse_ast_tree, default_options):
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Ensures that complexity is counted correctly.'
    tree_without_types = parse_ast_tree(line_simple)
    tree_with_types = parse_ast_tree(line_with_types)
    simple_visitor = JonesComplexityVisitor(default_options, tree=tree_without_types)
    typed_visitor = JonesComplexityVisitor(default_options, tree=tree_with_types)
    simple_visitor.run()
    typed_visitor.run()
    assert len(simple_visitor._lines) == 1
    assert len(simple_visitor._lines[1]) == 3
    assert len(typed_visitor._lines[1]) == 3

@pytest.mark.parametrize(('code', 'complexity'), [(line_with_comprehension, 6), (line_with_math, 9), (regression1216, 15)])
def test_exact_complexity(parse_ast_tree, default_options, code, complexity):
    (code, complexity) = (line_with_comprehension, 6)
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Ensures that complexity is counted correctly.'
    tree = parse_ast_tree(code)
    visitor = JonesComplexityVisitor(default_options, tree=tree)
    visitor.run()
    assert len(visitor._lines) == 1
    assert len(visitor._lines[1]) == complexity

@pytest.mark.parametrize(('code', 'number_of_lines'), [(line_inside_function, 1), (line_inside_async_function, 1), (class_with_async_function, 2), (class_with_function, 2), (class_with_usual_and_async_function, 3), (regression1216, 1)])
def test_that_some_nodes_are_ignored(parse_ast_tree, default_options, code, number_of_lines):
    (code, number_of_lines) = (line_inside_function, 1)
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Ensures that complexity is counted correctly.'
    tree = parse_ast_tree(code)
    visitor = JonesComplexityVisitor(default_options, tree=tree)
    visitor.run()
    assert len(visitor._lines) == number_of_lines
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