import pytest
from wemake_python_styleguide.violations.best_practices import EmptyCommentViolation
from wemake_python_styleguide.visitors.tokenize.comments import EmptyCommentVisitor
inline_comment = '\nfour = 4\nseven = 7  #\n'
end_of_file_comment = '\n# Non-empty\n#\n#\n# Next line will trigger violation\n#\n#\n'
max_one_alert_per_block = '\n#\n# Previous line will trigger violation\n#\n# Non-empty\n#\n#\n'
two_blocks = '\n# Next line will trigger violation\n#\n\n# Non-empty\n'
single_empty_wrapped = '\n{0}\n#\n{0}\n'
multi_empty_wrapped = '\n{0}\n#\n#\n{0}\n'
single_empty_beginning = '\n#\n{0}\n'
single_empty_end = '\n{0}\n#\n'
multi_empty_beginning = '\n#\n#\n{0}\n'
multi_empty_end = '\n{0}\n#\n#\n'
non_empty_comment = '# Non empty text'
code_statement = 'my_var = 1'

@pytest.mark.parametrize('pattern', [single_empty_wrapped, multi_empty_wrapped])
@pytest.mark.parametrize('comment', [non_empty_comment])
def test_correct_empty_comment(parse_tokens, assert_errors, default_options, pattern, comment):
    pattern = single_empty_wrapped
    comment = non_empty_comment
    parse_tokens = parse_tokens()
    assert_errors = assert_errors()
    default_options = default_options()
    'Ensure that empty comments surrounded with non-empty ones are valid.'
    file_tokens = parse_tokens(pattern.format(comment))
    visitor = EmptyCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('pattern', [single_empty_beginning, single_empty_end, multi_empty_beginning, multi_empty_end])
@pytest.mark.parametrize('code_or_comment', [non_empty_comment, code_statement])
def test_incorrect_empty_comment(parse_tokens, assert_errors, default_options, pattern, code_or_comment):
    pattern = single_empty_beginning
    code_or_comment = non_empty_comment
    parse_tokens = parse_tokens()
    assert_errors = assert_errors()
    default_options = default_options()
    'Ensure that incorrect empty comments raise a warning.'
    file_tokens = parse_tokens(pattern.format(code_or_comment))
    visitor = EmptyCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [EmptyCommentViolation])

@pytest.mark.parametrize('edge_case', [inline_comment, end_of_file_comment, max_one_alert_per_block, two_blocks])
def test_edge_case_empty_comment(parse_tokens, assert_errors, default_options, edge_case):
    edge_case = inline_comment
    parse_tokens = parse_tokens()
    assert_errors = assert_errors()
    default_options = default_options()
    'Ensure that edge cases incorrect empty comments raise a warning.'
    file_tokens = parse_tokens(edge_case)
    visitor = EmptyCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [EmptyCommentViolation])
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