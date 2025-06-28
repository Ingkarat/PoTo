import pytest
from wemake_python_styleguide.visitors.ast.statements import ParametersIndentationViolation, WrongParametersIndentationVisitor
correct_single_line_tuple = 'xy = (1, 2, 3)'
correct_single_line_list = 'xy = [1, 2, 3]'
correct_single_line_set = 'xy = {1, 2, 3}'
correct_single_line_dict = 'xy = {"key": [1, 2], "other": {1, 2}, "w": (1, 2)}'
correct_multiline_string = "\nxy = (\n    'first'\n    'second'\n    'last'\n)\n"
correct_multi_line_tuple = '\nxy = (\n    1,\n    2,\n    3,\n)\n'
correct_multi_line_list = '\nxy = [\n    1,\n    2,\n    3,\n]\n'
correct_multi_line_set = '\nxy = {\n    1,\n    2,\n    3,\n}\n'
correct_multi_line_dict = '\nxy = {\n    1: 1,\n    2: 2,\n    3: 3,\n}\n'
correct_next_line_tuple = '\nxy = (\n    1, 2, 3,\n)\n'
correct_next_line_list = '\nxy = [\n    1, 2, 3,\n]\n'
correct_next_line_set = '\nxy = {\n    1, 2, 3,\n}\n'
correct_next_line_tuple = '\nxy = {\n    1: 1, 2: 2, 3: 3,\n}\n'
correct_nested_collections = "\nxy = {\n    'key': [\n        1, 2, 3,\n    ],\n    'other': (\n        'first',\n        'second',\n    ),\n    'single': {1, 2, 3},\n    'multiple': {\n        1: [\n            1,\n            1,\n            1,\n        ],\n    },\n    'ending': 5,\n}\n"
correct_simple_regression450 = '\nwas_crashing = {**some_other_dict}\n'
correct_multiline_regression450 = '\nwas_crashing = {\n    **some_other_dict,\n    **some_very_other_dict,\n    **third_dict,\n}\n'
wrong_tuple_indentation1 = '\nxy = (1,\n      2, 3)\n'
wrong_tuple_indentation2 = '\nxy = (1, 2,\n      3)\n'
wrong_tuple_indentation3 = '\nxy = (\n    1, 2,\n    3,\n)\n'
wrong_tuple_indentation4 = '\nxy = (\n    1,\n    2, 3,\n)\n'
wrong_list_indentation1 = '\nxy = [1,\n      2, 3]\n'
wrong_list_indentation2 = '\nxy = [1, 2,\n      3]\n'
wrong_list_indentation3 = '\nxy = [\n    1, 2,\n    3,\n]\n'
wrong_list_indentation4 = '\nxy = [\n    1,\n    2, 3,\n]\n'
wrong_set_indentation1 = '\nxy = {1,\n      2, 3}\n'
wrong_set_indentation2 = '\nxy = {1, 2,\n      3}\n'
wrong_set_indentation3 = '\nxy = {\n    1, 2,\n    3,\n}\n'
wrong_set_indentation4 = '\nxy = {\n    1,\n    2, 3,\n}\n'
wrong_dict_indentation1 = '\nxy = {1: 1,\n      2: 2, 3: 3}\n'
wrong_dict_indentation2 = '\nxy = {1: 1, 2: 2,\n      3: 3}\n'
wrong_dict_indentation3 = '\nxy = {\n    1: 1, 2: 2,\n    3: 3,\n}\n'
wrong_dict_indentation4 = '\nxy = {\n    1: 1,\n    2: 2, 3: 3,\n}\n'
wrong_regression450 = '\nsome_dict = {\n    **one,\n    **two, **three,\n}\n'

@pytest.mark.parametrize('code', [correct_multiline_string, correct_single_line_tuple, correct_single_line_list, correct_single_line_set, correct_single_line_dict, correct_multi_line_tuple, correct_multi_line_list, correct_multi_line_set, correct_multi_line_dict, correct_next_line_list, correct_next_line_set, correct_next_line_tuple, correct_nested_collections, correct_simple_regression450, correct_multiline_regression450])
def test_correct_collection_indentation(assert_errors, parse_ast_tree, code, default_options):
    code = correct_multiline_string
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that correctly indented collections work.'
    tree = parse_ast_tree(code)
    visitor = WrongParametersIndentationVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [wrong_tuple_indentation1, wrong_tuple_indentation2, wrong_tuple_indentation3, wrong_tuple_indentation4, wrong_list_indentation1, wrong_list_indentation2, wrong_list_indentation3, wrong_list_indentation4, wrong_set_indentation1, wrong_set_indentation2, wrong_set_indentation3, wrong_set_indentation4, wrong_dict_indentation1, wrong_dict_indentation2, wrong_dict_indentation3, wrong_dict_indentation4, wrong_regression450])
def test_wrong_collection_indentation(assert_errors, parse_ast_tree, code, default_options):
    code = wrong_tuple_indentation1
    assert_errors = assert_errors()
    parse_ast_tree = parse_ast_tree()
    default_options = default_options()
    'Testing that poorly indented collections do not work.'
    tree = parse_ast_tree(code)
    visitor = WrongParametersIndentationVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [ParametersIndentationViolation])
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