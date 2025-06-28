import pytest
pytest
from mock import MagicMock
import bokeh.command.subcommand as sc

def test_is_abstract() -> None:
    with pytest.raises(TypeError):
        _Bad()

def test_missing_args() -> None:
    p = MagicMock()
    _Good(p)
    p.add_argument.assert_not_called()

def test_no_args() -> None:
    _Good.args = ()
    p = MagicMock()
    _Good(p)
    p.add_argument.assert_not_called()

def test_one_arg() -> None:
    _Good.args = (('foo', dict(a=1, b=2)),)
    p = MagicMock()
    _Good(p)
    p.add_argument.assert_called_once_with('foo', **dict(a=1, b=2))

def test_args() -> None:
    _Good.args = (('foo', dict(a=1, b=2)), ('bar', dict(a=3, b=4)))
    p = MagicMock()
    _Good(p)
    p.call_count == 2

def test_base_invoke() -> None:
    with pytest.raises(NotImplementedError):
        p = MagicMock()
        obj = _Good(p)
        super(_Good, obj).invoke('foo')

def _Good_invoke(self, args):
    pass