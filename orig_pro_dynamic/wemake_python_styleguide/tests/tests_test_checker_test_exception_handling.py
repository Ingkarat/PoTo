import ast
from contextlib import suppress
from wemake_python_styleguide.checker import Checker
from wemake_python_styleguide.violations.system import InternalErrorViolation
from wemake_python_styleguide.visitors.base import BaseNodeVisitor

class _BrokenVisitor(BaseNodeVisitor):

    def visit(self, _tree) -> None:
        raise ValueError('Message from visitor')

def test_exception_handling(default_options, capsys):
    default_options = default_options()
    'Ensures that checker works with module names.'
    Checker.parse_options(default_options)
    checker = Checker(tree=ast.parse(''), file_tokens=[], filename='test.py')
    checker._visitors = [_BrokenVisitor]
    with suppress(StopIteration):
        violation = next(checker.run())
        assert violation[2][7:] == InternalErrorViolation.error_template
    captured = capsys.readouterr()
    assert 'ValueError: Message from visitor' in captured.out
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