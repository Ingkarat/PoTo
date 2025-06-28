import pytest
from wemake_python_styleguide.violations.consistency import ImplicitRawStringViolation, UnicodeStringViolation, UppercaseStringModifierViolation
from wemake_python_styleguide.visitors.tokenize.primitives import WrongStringTokenVisitor

@pytest.mark.parametrize('code', ["'\\\\a'", "'\\\\n'", "'\\\\\\\\'", "'some \\\\ escaped'", "b'\\\\a'", '"""\\\\1"""', "'''\\\\ '''"])
def test_implicit_raw_string(parse_tokens, assert_errors, default_options, code):
    code = "'\\\\a'"
    parse_tokens = parse_tokens()
    assert_errors = assert_errors()
    default_options = default_options()
    'Ensures that implicit raw strings raise a warning.'
    file_tokens = parse_tokens(code)
    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [ImplicitRawStringViolation])

@pytest.mark.parametrize('code', ["'\\\\'", "r'\\\\'", "'\\n'", "r'\\n'", "r'some \\\\ escaped'", "r'some \\n escaped'", "br'\\\\a'", 'r"""\\\\text"""', "r'''\\\\ '''"])
def test_explicit_raw_string(parse_tokens, assert_errors, default_options, code):
    code = "'\\\\'"
    parse_tokens = parse_tokens()
    assert_errors = assert_errors()
    default_options = default_options()
    'Ensures that implicit raw strings raise a warning.'
    file_tokens = parse_tokens(code)
    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('code', ["u'\\\\4'", "u'\\\\n'", "u'\\\\\\\\'", "u'some \\\\ escaped'"])
def test_implicit_unicode_raw_string(parse_tokens, assert_errors, default_options, code):
    code = "u'\\\\4'"
    parse_tokens = parse_tokens()
    assert_errors = assert_errors()
    default_options = default_options()
    'Ensures that implicit unicode raw string raise a warning.'
    file_tokens = parse_tokens(code)
    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [UnicodeStringViolation, ImplicitRawStringViolation])

@pytest.mark.parametrize('code', ["U'\\\\4'", "U'\\\\n'", "U'\\\\\\\\'", "U'some \\\\ escaped'"])
def test_implicit_uppercase_unicode_raw_string(parse_tokens, assert_errors, default_options, code):
    code = "U'\\\\4'"
    parse_tokens = parse_tokens()
    assert_errors = assert_errors()
    default_options = default_options()
    'Ensures that implicit uppercase unicode raw string raise a warning.'
    file_tokens = parse_tokens(code)
    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [UnicodeStringViolation, UppercaseStringModifierViolation, ImplicitRawStringViolation])
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