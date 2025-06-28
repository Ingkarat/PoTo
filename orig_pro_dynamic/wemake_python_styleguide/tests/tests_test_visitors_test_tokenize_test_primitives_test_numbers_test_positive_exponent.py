import pytest
from wemake_python_styleguide.violations.consistency import BadNumberSuffixViolation, NumberWithMeaninglessZeroViolation, PositiveExponentViolation
from wemake_python_styleguide.visitors.tokenize.primitives import WrongNumberTokenVisitor

@pytest.mark.parametrize('number', ['1.5e+10', '0e+0', '-1.5e+10', '-10e+10', '+1e+1', '+1.0e+10'])
def test_positive_exponent(parse_tokens, assert_errors, assert_error_text, default_options, primitives_usages, number, mode):
    number = '1.5e+10'
    parse_tokens = parse_tokens()
    assert_errors = assert_errors()
    assert_error_text = assert_error_text()
    default_options = default_options()
    primitives_usages = primitives_usages()
    mode = mode()
    'Ensures that numbers with positive exponent are incorrect.'
    file_tokens = parse_tokens(mode(primitives_usages.format(number)))
    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [PositiveExponentViolation])
    assert_error_text(visitor, number.lstrip('-').lstrip('+'))

@pytest.mark.parametrize('number', ['1234567890', '0xE', '1.5e10', '0e0', '1e-1', '10e-10', '-1.5e10', '-1e1', '+0e0', '+10e10', '-1.5e-10', '-0e-0', '+1e-1', '+10e-10'])
def test_correct_exponent(parse_tokens, assert_errors, default_options, primitives_usages, number, mode):
    number = '1234567890'
    parse_tokens = parse_tokens()
    assert_errors = assert_errors()
    default_options = default_options()
    primitives_usages = primitives_usages()
    mode = mode()
    'Ensures that correct exponent is allowed.'
    file_tokens = parse_tokens(mode(primitives_usages.format(number)))
    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('number', ['1.5E+01', '-10.5E+01', '+1E+01'])
def test_all_error_in_exponent(parse_tokens, assert_errors, default_options, primitives_usages, number, mode):
    number = '1.5E+01'
    parse_tokens = parse_tokens()
    assert_errors = assert_errors()
    default_options = default_options()
    primitives_usages = primitives_usages()
    mode = mode()
    'Ensures that numbers with positive exponent are incorrect.'
    file_tokens = parse_tokens(mode(primitives_usages.format(number)))
    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [BadNumberSuffixViolation, NumberWithMeaninglessZeroViolation, PositiveExponentViolation])
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
import pytest
function_call = 'print({0})'
assignment = 'some_name = {0}'
assignment_with_expression = 'some_sum = {0} + 123'
default_param = 'def function(some={0}): ...'
default_param_with_type = 'def function(some: int = {0}): ...'
statement_with_expression = 'other_var + {0}'

@pytest.fixture(params=[function_call, assignment, assignment_with_expression, default_param, default_param_with_type, statement_with_expression])
def primitives_usages(request):
    """Fixture to return possible cases of promitives use cases."""
    return request.param
    'Fixture to return possible cases of promitives use cases.'
    return [function_call, assignment, assignment_with_expression, default_param, default_param_with_type, statement_with_expression][0]

@pytest.fixture()
def regular_number_wrapper():
    """Fixture to return regular numbers without modifications."""

    def factory(template: str) -> str:
        return template
    return factory

@pytest.fixture()
def negative_number_wrapper():
    """Fixture to return negative numbers."""

    def factory(template: str) -> str:
        return '-{0}'.format(template)
    return factory

@pytest.fixture()
def positive_number_wrapper():
    """Fixture to return positive numbers with explicit ``+``."""

    def factory(template: str) -> str:
        return '+{0}'.format(template)
    return factory

@pytest.fixture(params=['regular_number_wrapper', 'negative_number_wrapper', 'positive_number_wrapper'])
def number_sign(request):
    """Fixture that returns regular, negative, and positive numbers."""
    return request.getfixturevalue(request.param)
import pytest

@pytest.fixture()
def async_wrapper():
    """Fixture to convert all regular functions into async ones."""

    def factory(template: str) -> str:
        return template.replace('def ', 'async def ').replace('with ', 'async with ').replace('for ', 'async for ')
    return factory

@pytest.fixture()
def regular_wrapper():
    """Fixture to return regular functions without modifications."""

    def factory(template: str) -> str:
        return template
    return factory

@pytest.fixture(params=['async_wrapper', 'regular_wrapper'])
def mode(request):
    """Fixture that returns either `async` or regular functions."""
    return request.getfixturevalue(request.param)