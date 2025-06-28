import pytest
from wemake_python_styleguide.violations.best_practices import ShebangViolation
from wemake_python_styleguide.visitors.tokenize import comments
template_empty = ''
template_newlines = '\n\n'
template_regular = '{0}'
template_with_leading_comment = '{0}\n# some other\n'
template_regular_comment = 'x = 1{0}'

@pytest.mark.parametrize('template', [template_regular, template_with_leading_comment])
@pytest.mark.parametrize(('code', 'executable'), [('x = 1', False), ('#!/bin/python', True)])
def test_correct_shebang_executable1(make_file, assert_errors, parse_file_tokens, default_options, template, code, executable):
    template = template_regular
    (code, executable) = ('x = 1', False)
    make_file = make_file()
    assert_errors = assert_errors()
    parse_file_tokens = parse_file_tokens()
    default_options = default_options()
    'Testing cases when no errors should be reported.'
    path_to_file = make_file('test_file.py', template.format(code), executable)
    file_tokens = parse_file_tokens(path_to_file)
    visitor = comments.ShebangVisitor(default_options, filename=path_to_file, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('template', [template_regular_comment, template_empty])
@pytest.mark.parametrize(('code', 'executable'), [('#!/bin/some', False), ('#!/bin/python', False), ('# any text', False), ('   # any text with padding', False)])
def test_correct_shebang_executable2(make_file, assert_errors, parse_file_tokens, default_options, template, code, executable):
    template = template_regular_comment
    (code, executable) = ('#!/bin/some', False)
    make_file = make_file()
    assert_errors = assert_errors()
    parse_file_tokens = parse_file_tokens()
    default_options = default_options()
    'Testing cases when no errors should be reported.'
    path_to_file = make_file('test_file.py', template.format(code), executable)
    file_tokens = parse_file_tokens(path_to_file)
    visitor = comments.ShebangVisitor(default_options, filename=path_to_file, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('template', [template_regular, template_with_leading_comment, template_regular_comment, template_empty])
@pytest.mark.parametrize(('code', 'executable'), [('#!/bin/python', False), ('#!/bin/python', True), ('# any text', False), ('# any text', True)])
def test_shebang_on_windows(make_file, monkeypatch, assert_errors, parse_file_tokens, default_options, template, code, executable):
    template = template_regular
    (code, executable) = ('#!/bin/python', False)
    make_file = make_file()
    assert_errors = assert_errors()
    parse_file_tokens = parse_file_tokens()
    default_options = default_options()
    'Testing cases when no errors should be reported.'
    monkeypatch.setattr(comments, 'is_windows', lambda : True)
    path_to_file = make_file('test_file.py', template.format(code), executable)
    file_tokens = parse_file_tokens(path_to_file)
    visitor = comments.ShebangVisitor(default_options, filename=path_to_file, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('template', [template_regular, template_with_leading_comment, template_regular_comment, template_empty])
@pytest.mark.parametrize(('code', 'executable'), [('#!/bin/python', False), ('#!/bin/python', True), ('# any text', False), ('# any text', True)])
def test_shebang_with_stdin(make_file, monkeypatch, assert_errors, parse_file_tokens, default_options, template, code, executable):
    template = template_regular
    (code, executable) = ('#!/bin/python', False)
    make_file = make_file()
    assert_errors = assert_errors()
    parse_file_tokens = parse_file_tokens()
    default_options = default_options()
    'Testing cases when no errors should be reported.'
    path_to_file = make_file('test_file.py', template.format(code), executable)
    file_tokens = parse_file_tokens(path_to_file)
    visitor = comments.ShebangVisitor(default_options, filename='stdin', file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('template', [template_regular, template_with_leading_comment])
@pytest.mark.parametrize(('code', 'executable'), [('#!/bin/python', False), ('# regular comment', True)])
def test_wrong_shebang_executable(make_file, assert_errors, parse_file_tokens, default_options, template, code, executable):
    template = template_regular
    (code, executable) = ('#!/bin/python', False)
    make_file = make_file()
    assert_errors = assert_errors()
    parse_file_tokens = parse_file_tokens()
    default_options = default_options()
    'Testing cases when no errors should be reported.'
    path_to_file = make_file('test_file.py', template.format(code), executable)
    file_tokens = parse_file_tokens(path_to_file)
    visitor = comments.ShebangVisitor(default_options, filename=path_to_file, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [ShebangViolation])

@pytest.mark.parametrize('template', [template_with_leading_comment])
@pytest.mark.parametrize('code', ['#!/bin/other', ' #!/bin/python', '\n\n#!python'])
def test_wrong_shebang_format(make_file, assert_errors, parse_file_tokens, default_options, template, code):
    template = template_with_leading_comment
    code = '#!/bin/other'
    make_file = make_file()
    assert_errors = assert_errors()
    parse_file_tokens = parse_file_tokens()
    default_options = default_options()
    'Testing cases when no errors should be reported.'
    path_to_file = make_file('test_file.py', template.format(code), is_executable=True)
    file_tokens = parse_file_tokens(path_to_file)
    visitor = comments.ShebangVisitor(default_options, filename=path_to_file, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [ShebangViolation])
from os import chmod
import pytest
TEMP_FOLDER = 'tmp'
MODE_EXECUTABLE = 493
MODE_NON_EXECUTABLE = 420

@pytest.fixture()
def make_file(tmp_path):
    """Fixture to make a temporary executable or non executable file."""

    def factory(filename: str, file_content: str, is_executable: bool) -> str:
        temp_folder = tmp_path / TEMP_FOLDER
        temp_folder.mkdir()
        test_file = temp_folder / filename
        file_mode = MODE_EXECUTABLE if is_executable else MODE_NON_EXECUTABLE
        test_file.write_text(file_content)
        chmod(test_file.as_posix(), file_mode)
        return test_file.as_posix()
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