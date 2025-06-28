import subprocess

def test_invalid_options(absolute_path):
    absolute_path = absolute_path()
    'End-to-End test to check option validation works.'
    process = subprocess.Popen(['flake8', '--isolated', '--select', 'WPS', '--max-imports', '-5', absolute_path('fixtures', 'noqa.py')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding='utf8')
    (_, stderr) = process.communicate()
    assert process.returncode == 1
    assert 'ValueError' in stderr

def test_invalid_domain_names_options(absolute_path):
    absolute_path = absolute_path()
    'End-to-End test to check domain names options validation works.'
    process = subprocess.Popen(['flake8', '--isolated', '--select', 'WPS', '--allowed-domain-names', 'item,items,handle,visitor', '--forbidden-domain-names', 'handle,visitor,node', absolute_path('fixtures', 'noqa.py')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding='utf8')
    (_, stderr) = process.communicate()
    assert process.returncode == 1
    assert 'ValueError' in stderr
    assert 'handle' in stderr
    assert 'visitor' in stderr
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