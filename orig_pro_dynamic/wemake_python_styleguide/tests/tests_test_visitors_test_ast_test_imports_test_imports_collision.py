import pytest
from wemake_python_styleguide.violations.best_practices import ImportCollisionViolation
from wemake_python_styleguide.violations.consistency import DottedRawImportViolation, LocalFolderImportViolation
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor
correct_single_import = 'import public'
correct_single_import_from = 'from utils import public'
correct_no_colliding_imports = '\nfrom other import public\nfrom other.module import something\n'
correct_similar_imports = '\nimport ast\nimport astor\n'
correct_no_colliding_imports_from = '\nfrom utils import public\nfrom other import something\n'
correct_import_with_alias = '\nimport public\nfrom public import something as sth\n'
correct_import_from_with_alias = '\nfrom utils import public\nfrom utils.public.others import something as sth\n'
correct_multiple_imports_from = '\nfrom utils import public\nfrom utils.public.module import something as sth, something_else\n'
correct_imports_from = '\nfrom utils import public\nfrom utils.public.module import something\n'
correct_import_name_module_part = '\nimport public\nfrom public.module import something\n'
correct_relative_import = '\nfrom . import first as _my\nfrom first import other\n'
colliding_same_line = 'import abc, abc.ABC'
colliding_import_name_module = '\nimport public\nfrom public import something\n'
colliding_multiple_imports = '\nimport public, foo, bar as baz\nfrom public import something\n'
colliding_multiple_imports_from = '\nfrom utils import public, foo, bar as baz\nfrom utils.public import something\n'
colliding_relative_import1 = '\nfrom . import first\nfrom first import other\n'
colliding_relative_import2 = '\nfrom .. import first\nfrom first import other\n'

@pytest.mark.parametrize('code', [correct_single_import, correct_single_import_from, correct_no_colliding_imports, correct_similar_imports, correct_no_colliding_imports_from, correct_import_with_alias, correct_import_from_with_alias, correct_multiple_imports_from, correct_imports_from, correct_import_name_module_part, correct_relative_import])
def test_correct_imports(assert_errors, parse_ast_tree, code, default_options):
    code = correct_single_import
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that no colliding imports are allowed.'
    tree = parse_ast_tree(code)
    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [], ignored_types=LocalFolderImportViolation)

@pytest.mark.parametrize('code', [colliding_same_line, colliding_import_name_module, colliding_multiple_imports, colliding_multiple_imports_from, colliding_relative_import1, colliding_relative_import2])
def test_imports_collision(assert_errors, parse_ast_tree, code, default_options):
    code = colliding_same_line
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that colliding imports are restricted.'
    tree = parse_ast_tree(code)
    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [ImportCollisionViolation], ignored_types=(DottedRawImportViolation, LocalFolderImportViolation))
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