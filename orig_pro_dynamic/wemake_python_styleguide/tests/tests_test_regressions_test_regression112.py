import ast
from pyflakes.checker import Checker as PyFlakesChecker
from wemake_python_styleguide.checker import Checker
code_that_breaks = '\ndef current_session(\n    telegram_id: int,\n    for_update: bool = True,\n) -> TelegramSession:\n    """\n    Was triggering `AttributeError`.\n\n    See: https://github.com/wemake-services/wemake-python-styleguide/issues/112\n    """\n    try:\n        query = TelegramSession.objects.all()\n        if for_update:  # Try to comment this `if` to fix everything\n            query = query.select_for_update()\n\n        return query.get(\n            uid=telegram_id,\n            is_verified=True,\n        )\n\n    except TelegramSession.DoesNotExist:\n        raise AuthenticationException(\'Session is missing\')\n'

def test_regression112(default_options):
    default_options = default_options()
    '\n    There was a conflict between ``pyflakes`` and our plugin.\n\n    We were fighting for ``parent`` property.\n    Now we use a custom prefix.\n\n    See: https://github.com/wemake-services/wemake-python-styleguide/issues/112\n    '
    module = ast.parse(code_that_breaks)
    Checker.parse_options(default_options)
    Checker(tree=module, file_tokens=[], filename='custom.py')
    flakes = PyFlakesChecker(module)
    assert module.wps_context is None
    assert flakes.root
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