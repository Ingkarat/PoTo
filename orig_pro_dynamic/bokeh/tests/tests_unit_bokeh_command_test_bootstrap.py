import pytest
pytest
from bokeh import __version__
from bokeh.command.bootstrap import main

def _assert_version_output(capsys):
    (out, err) = capsys.readouterr()
    err_expected = ''
    out_expected = '%s\n' % __version__
    assert err == err_expected
    assert out == out_expected

def test_no_subcommand(capsys) -> None:
    with pytest.raises(SystemExit):
        main(['bokeh'])
    (out, err) = capsys.readouterr()
    assert err == 'ERROR: Must specify subcommand, one of: build, info, init, json, sampledata, secret, serve or static\n'
    assert out == ''

def test_version(capsys) -> None:
    with pytest.raises(SystemExit):
        main(['bokeh', '--version'])
    _assert_version_output(capsys)

def test_version_short(capsys) -> None:
    with pytest.raises(SystemExit):
        main(['bokeh', '-v'])
    _assert_version_output(capsys)

def test_error(capsys) -> None:
    from bokeh.command.subcommands.info import Info
    old_invoke = Info.invoke

    def err(x, y):
        raise RuntimeError('foo')
    Info.invoke = err
    with pytest.raises(SystemExit):
        main(['bokeh', 'info'])
    (out, err) = capsys.readouterr()
    assert err == 'ERROR: foo\n'
    Info.invoke = old_invoke