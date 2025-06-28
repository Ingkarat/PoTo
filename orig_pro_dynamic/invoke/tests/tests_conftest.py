import logging
import os
import sys
import termios
from invoke.vendor.six import iteritems
import pytest
from mock import patch
from _util import support
logging.basicConfig(level=logging.INFO)

@pytest.fixture
def reset_environ():
    """
    Resets `os.environ` to its prior state after the fixtured test finishes.
    """
    old_environ = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(old_environ)

@pytest.fixture
def chdir_support():
    os.chdir(support)
    yield
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def clean_sys_modules():
    yield
    for (name, module) in iteritems(sys.modules.copy()):
        if module and support in (getattr(module, '__file__', '') or ''):
            del sys.modules[name]

@pytest.fixture
def integration(reset_environ, chdir_support, clean_sys_modules):
    yield

@pytest.fixture
def mock_termios():
    with patch('invoke.terminals.termios') as mocked:
        mocked.ECHO = termios.ECHO
        mocked.ICANON = termios.ICANON
        mocked.VMIN = termios.VMIN
        mocked.VTIME = termios.VTIME
        yield mocked