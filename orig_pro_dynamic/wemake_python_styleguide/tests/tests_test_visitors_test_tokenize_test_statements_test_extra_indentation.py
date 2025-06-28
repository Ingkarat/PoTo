import pytest
from wemake_python_styleguide.violations.consistency import ExtraIndentationViolation
from wemake_python_styleguide.visitors.tokenize.statements import ExtraIndentationVisitor
correct_function_with_docstring = "\ndef first():\n    '''Some text'''\n    return None\n"
correct_multiple_functions = '\ndef first():\n    if some:\n        return 1\n    return 2\n\ndef second(args: Tuple[int, int]) -> None:\n    print(\n        args[0],\n        args[1],\n    )\n'
correct_multiline_tuple = '\nsome = (\n    [1, 1, 1],\n    2,\n    3,\n)\n'
correct_multiline_dict = '\nsome = {\n    1: [\n        1,\n        1,\n        1,\n    ],\n    2: 2,\n    3: 3,\n}\n'
correct_multiline_call = "\nprint(\n    'a',\n    object(),\n    [2, 3],\n)\n"
wrong_function_with_docstring = "\ndef first():\n        '''Some text'''\n        return None\n"
wrong_multiple_functions = '\ndef first():\n    if some:\n            return 1\n    return 2\n\ndef second(args: Tuple[int, int]) -> None:\n    print(\n        args[0],\n        args[1],\n    )\n'
wrong_multiline_tuple = '\nsome = (\n        [1, 1, 1],\n        2,\n        3,\n)\n'
wrong_multiline_dict = '\nsome = {\n        1: [\n            1,\n            1,\n            1,\n        ],\n        2: 2,\n        3: 3,\n}\n'
wrong_multiline_call = "\nprint(\n            'a',\n            object(),\n            [2, 3],\n)\n"
wrong_single_paren = '\nsome_set = {1\n           }\n'

@pytest.mark.parametrize('code', [correct_function_with_docstring, correct_multiple_functions, correct_multiline_tuple, correct_multiline_dict, correct_multiline_call])
def test_correct_indentation(parse_tokens, assert_errors, default_options, code):
    code = correct_function_with_docstring
    parse_tokens = parse_tokens()
    assert_errors = assert_errors()
    default_options = default_options()
    'Ensures that correct indentation works.'
    file_tokens = parse_tokens(code)
    visitor = ExtraIndentationVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', [wrong_function_with_docstring, wrong_multiple_functions, wrong_multiline_tuple, wrong_multiline_dict, wrong_multiline_call, wrong_single_paren])
def test_wrong_indentation(parse_tokens, assert_errors, default_options, code):
    code = wrong_function_with_docstring
    parse_tokens = parse_tokens()
    assert_errors = assert_errors()
    default_options = default_options()
    'Ensures that incorrect indentation raises a warning.'
    file_tokens = parse_tokens(code)
    visitor = ExtraIndentationVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [ExtraIndentationViolation])
import io
import tokenize
from textwrap import dedent
import pytest

@pytest.fixture(scope='session')
def parse_tokens():
    """Parses tokens from a string."""

    def factory(code: str):
        lines = io.StringIO(dedent(code))
        return list(tokenize.generate_tokens(lambda : next(lines)))
    return factory

@pytest.fixture(scope='session')
def parse_file_tokens(parse_tokens):
    """Parses tokens from a file."""

    def factory(filename: str):
        with open(filename, 'r', encoding='utf-8') as test_file:
            file_content = test_file.read()
            return parse_tokens(file_content)
    return factory
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