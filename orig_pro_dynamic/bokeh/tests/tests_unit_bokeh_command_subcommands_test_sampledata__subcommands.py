import pytest
pytest
from bokeh.command.bootstrap import main
import bokeh.command.subcommands.sampledata as scsample
did_call_download = False

def test_create() -> None:
    import argparse
    from bokeh.command.subcommand import Subcommand
    obj = scsample.Sampledata(parser=argparse.ArgumentParser())
    assert isinstance(obj, Subcommand)

def test_name() -> None:
    assert scsample.Sampledata.name == 'sampledata'

def test_help() -> None:
    assert scsample.Sampledata.help == 'Download the bokeh sample data sets'

def test_args() -> None:
    assert scsample.Sampledata.args == ()

def test_run(capsys) -> None:
    main(['bokeh', 'sampledata'])
    assert did_call_download == True

def _mock_download():
    global did_call_download
    did_call_download = True
scsample.sampledata.download = _mock_download