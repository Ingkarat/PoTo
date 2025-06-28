import pytest
from wemake_python_styleguide.constants import MODULE_NAMES_BLACKLIST
from wemake_python_styleguide.violations.naming import WrongModuleNameViolation
from wemake_python_styleguide.visitors.filenames.module import WrongModuleNameVisitor

@pytest.mark.parametrize('filename', ['query.py', '/home/user/logic.py', 'partial/views.py', 'C:/path/package/module.py'])
def test_simple_filename(assert_errors, filename, default_options):
    filename = 'query.py'
    assert_errors = assert_errors()
    default_options = default_options()
    'Testing that simple file names works well.'
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()
    assert_errors(visitor, [])

@pytest.mark.parametrize('filename', MODULE_NAMES_BLACKLIST)
def test_restricted_filename(assert_errors, filename, default_options):
    filename = MODULE_NAMES_BLACKLIST[0]
    assert_errors = assert_errors()
    default_options = default_options()
    'Testing that some file names are restricted.'
    visitor = WrongModuleNameVisitor(default_options, filename='{0}.py'.format(filename))
    visitor.run()
    assert_errors(visitor, [WrongModuleNameViolation])
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