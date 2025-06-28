"""
This is a regression test for the argument parsing issue for boolean args.

.. versionadded:: 0.13.0

See also:
    - https://github.com/wemake-services/wemake-python-styleguide/issues/966
    - https://stackoverflow.com/a/15008806/4842742

"""

def test_parsing_i_control_code(option_parser):
    option_parser = option_parser()
    'Ensures that ``i_control_code`` can be parsed.'
    (args, _) = option_parser.parse_args(['--i-control-code'])
    assert args.i_control_code is True

def test_parsing_i_dont_control_code(option_parser):
    option_parser = option_parser()
    'Ensures that ``i_dont_control_code`` can be parsed.'
    (args, _) = option_parser.parse_args(['--i-dont-control-code'])
    assert args.i_control_code is False
import pytest
from flake8.options.manager import OptionManager
from wemake_python_styleguide import version
from wemake_python_styleguide.options import config

@pytest.fixture()
def option_parser():
    """Returns option parser that can be used for tests."""
    parser = OptionManager(prog=version.pkg_name, version=version.pkg_version)
    config.Configuration().register_options(parser)
    return parser