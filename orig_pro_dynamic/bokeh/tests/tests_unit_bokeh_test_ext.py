import pytest
pytest
import os
import bokeh.ext as ext

@pytest.mark.skip(reason='error')
def test_ext_commands(tmpdir) -> None:
    tmp = str(tmpdir.mkdir('bk_ext_01'))
    assert _names(tmp) == []
    assert ext.init(tmp, bokehjs_version='1.3.4') is True
    assert _names(tmp) == ['bokeh.ext.json', 'index.ts', 'package.json', 'tsconfig.json']
    assert ext.build(tmp) is True
    assert _names(tmp) == ['.bokeh', 'bokeh.ext.json', 'dist', 'index.ts', 'node_modules', 'package-lock.json', 'package.json', 'tsconfig.json']
    assert ext.init(tmp) is False

def _entries(path):
    return sorted(os.scandir(path), key=lambda entry: entry.name)

def _names(path):
    return [entry.name for entry in _entries(path)]