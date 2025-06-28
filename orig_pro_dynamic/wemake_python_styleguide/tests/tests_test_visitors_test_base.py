from unittest.mock import MagicMock
from wemake_python_styleguide import constants
from wemake_python_styleguide.visitors.base import BaseFilenameVisitor

class _TestingFilenameVisitor(BaseFilenameVisitor):

    def visit_filename(self):
        """Overridden to satisfy abstract base class."""

def test_base_filename_run_do_not_call_visit(default_options):
    default_options = default_options()
    'Ensures that `run()` does not call `visit()` method for stdin.'
    instance = _TestingFilenameVisitor(default_options, filename=constants.STDIN)
    instance.visit_filename = MagicMock()
    instance.run()
    instance.visit_filename.assert_not_called()
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