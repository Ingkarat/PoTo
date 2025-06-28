import pytest
pytest
from bokeh.command.bootstrap import main
import bokeh.command.subcommands.secret as scsecret

def test_create() -> None:
    import argparse
    from bokeh.command.subcommand import Subcommand
    obj = scsecret.Secret(parser=argparse.ArgumentParser())
    assert isinstance(obj, Subcommand)

def test_name() -> None:
    assert scsecret.Secret.name == 'secret'

def test_help() -> None:
    assert scsecret.Secret.help == 'Create a Bokeh secret key for use with Bokeh server'

def test_args() -> None:
    assert scsecret.Secret.args == ()

def test_run(capsys) -> None:
    main(['bokeh', 'secret'])
    (out, err) = capsys.readouterr()
    assert err == ''
    assert len(out) == 45
    assert out[-1] == '\n'