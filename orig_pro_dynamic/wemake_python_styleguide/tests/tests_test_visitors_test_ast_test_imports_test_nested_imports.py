import pytest
from wemake_python_styleguide.violations.best_practices import NestedImportViolation
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor
nested_function_import = '\ndef function():\n    import os\n'
nested_function_from_import = '\ndef function():\n    from os import path\n'
nested_conditional_import = '\nif True:\n    import os\n'
nested_method_import = '\nclass Test(object):\n    def with_import(self):\n        import os\n'
nested_method_from_import = '\nclass Test(object):\n    def with_import(self):\n        from os import path\n'
nested_try_import = '\ntry:\n    from missing import some_thing\nexcept ImportError:\n    some_thing = None\n'
regular_import = 'import os'
regular_from_import = 'from os import path'
regular_nested_import = 'from core.violations import Error'
type_checking_import = '\nif TYPE_CHECKING:\n    from core.violations import Error\n'
typing_type_checking_import = '\nif typing.TYPE_CHECKING:\n    from core.violations import Error\n'

@pytest.mark.parametrize('code', [nested_function_import, nested_function_from_import, nested_method_import, nested_method_from_import, nested_conditional_import, nested_try_import])
def test_nested_import(assert_errors, parse_ast_tree, code, default_options):
    code = nested_function_import
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that nested imports are restricted.'
    tree = parse_ast_tree(code)
    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [NestedImportViolation])

@pytest.mark.parametrize('code', [regular_import, regular_from_import, regular_nested_import, type_checking_import, typing_type_checking_import])
def test_regular_imports(assert_errors, parse_ast_tree, code, default_options):
    code = regular_import
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    '\n    Testing imports that are allowed.\n\n    Regular imports are allowed.\n    Imports nested inside the TYPE_CHECKING check are allowed.\n    '
    tree = parse_ast_tree(code)
    visitor = WrongImportVisitor(default_options, tree=tree)
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