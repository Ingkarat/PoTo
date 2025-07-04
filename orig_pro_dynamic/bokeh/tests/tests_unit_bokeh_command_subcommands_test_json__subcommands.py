import pytest
pytest
import argparse
import os
from _util_subcommands import basic_scatter_script
from bokeh._testing.util.filesystem import TmpDir, WorkingDir, with_directory_contents
from bokeh.command.bootstrap import main
import bokeh.command.subcommands.json as scjson

def test_create() -> None:
    import argparse
    from bokeh.command.subcommand import Subcommand
    obj = scjson.JSON(parser=argparse.ArgumentParser())
    assert isinstance(obj, Subcommand)

def test_name() -> None:
    assert scjson.JSON.name == 'json'

def test_help() -> None:
    assert scjson.JSON.help == 'Create JSON files for one or more applications'

def test_args() -> None:
    assert scjson.JSON.args == (('files', dict(metavar='DIRECTORY-OR-SCRIPT', nargs='+', help='The app directories or scripts to generate JSON for', default=None)), ('--indent', dict(metavar='LEVEL', type=int, help='indentation to use when printing', default=None)), (('-o', '--output'), dict(metavar='FILENAME', action='append', type=str, help='Name of the output file or - for standard output.')), ('--args', dict(metavar='COMMAND-LINE-ARGS', nargs=argparse.REMAINDER, help='Any command line arguments remaining are passed on to the application handler')))

def test_no_script(capsys) -> None:
    with TmpDir(prefix='bokeh-json-no-script') as dirname:
        with WorkingDir(dirname):
            with pytest.raises(SystemExit):
                main(['bokeh', 'json'])
        (out, err) = capsys.readouterr()
        too_few = 'the following arguments are required: DIRECTORY-OR-SCRIPT'
        assert err == 'usage: bokeh json [-h] [--indent LEVEL] [-o FILENAME] [--args ...]\n                  DIRECTORY-OR-SCRIPT [DIRECTORY-OR-SCRIPT ...]\nbokeh json: error: %s\n' % too_few
        assert out == ''

def test_basic_script(capsys) -> None:

    def run(dirname):
        with WorkingDir(dirname):
            main(['bokeh', 'json', 'scatter.py'])
        (out, err) = capsys.readouterr()
        assert err == ''
        assert out == ''
        assert {'scatter.json', 'scatter.py'} == set(os.listdir(dirname))
    with_directory_contents({'scatter.py': basic_scatter_script}, run)

def test_basic_script_with_output_after(capsys) -> None:

    def run(dirname):
        with WorkingDir(dirname):
            main(['bokeh', 'json', 'scatter.py', '--output', 'foo.json'])
        (out, err) = capsys.readouterr()
        assert err == ''
        assert out == ''
        assert {'foo.json', 'scatter.py'} == set(os.listdir(dirname))
    with_directory_contents({'scatter.py': basic_scatter_script}, run)

def test_basic_script_with_output_before(capsys) -> None:

    def run(dirname):
        with WorkingDir(dirname):
            main(['bokeh', 'json', '--output', 'foo.json', 'scatter.py'])
        (out, err) = capsys.readouterr()
        assert err == ''
        assert out == ''
        assert {'foo.json', 'scatter.py'} == set(os.listdir(dirname))
    with_directory_contents({'scatter.py': basic_scatter_script}, run)