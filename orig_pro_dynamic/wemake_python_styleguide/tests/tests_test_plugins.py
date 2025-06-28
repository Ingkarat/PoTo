"""
These test ensures that each plugin is enabled and working.

We only test a single warning from each plugin.
We do not test that any of the 3rd party plugins work correctly.

It is not our responsibility.
"""
import subprocess
PLUGINS = ('B002', 'C400', 'C819', 'D103', 'E225', 'E800', 'F401', 'N400', 'N802', 'P101', 'Q003', 'S101', 'T100', 'RST215', 'DAR101')

def _assert_plugin_output(output):
    for plugin_code in PLUGINS:
        assert output.count(plugin_code) > 0

def test_external_plugins(absolute_path):
    absolute_path = absolute_path()
    'End-to-End test to check that all plugins are enabled.'
    filename = absolute_path('fixtures', 'external_plugins.py')
    process = subprocess.Popen(['flake8', '--isolated', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding='utf8')
    (output, _) = process.communicate()
    _assert_plugin_output(output)

def test_external_plugins_diff(absolute_path):
    absolute_path = absolute_path()
    'Ensures that our linter and all plugins work in ``diff`` mode.'
    process = subprocess.Popen(['diff', '-uN', 'missing_file', absolute_path('fixtures', 'external_plugins.py')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding='utf8')
    output = subprocess.check_output(['flake8', '--isolated', '--diff', '--exit-zero'], stdin=process.stdout, stderr=subprocess.PIPE, universal_newlines=True, encoding='utf8')
    process.communicate()
    _assert_plugin_output(output)
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