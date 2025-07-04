import pytest
pytest
import os
import tempfile
from mock import patch
from bokeh.document import Document
from bokeh.layouts import row
from bokeh.plotting import figure
import bokeh.command.util as util

def test_die(capsys) -> None:
    with pytest.raises(SystemExit):
        util.die('foo')
    (out, err) = capsys.readouterr()
    assert err == 'foo\n'
    assert out == ''

def test_build_single_handler_application_unknown_file() -> None:
    with pytest.raises(ValueError) as e:
        f = tempfile.NamedTemporaryFile(suffix='.bad')
        util.build_single_handler_application(f.name)
    assert "Expected a '.py' script or '.ipynb' notebook, got: " in str(e.value)

def test_build_single_handler_application_nonexistent_file() -> None:
    with pytest.raises(ValueError) as e:
        util.build_single_handler_application('junkjunkjunk')
    assert 'Path for Bokeh server application does not exist: ' in str(e.value)
DIRSTYLE_MAIN_WARNING_COPY = '\nIt looks like you might be running the main.py of a directory app directly.\nIf this is the case, to enable the features of directory style apps, you must\ncall "bokeh serve" on the directory instead. For example:\n\n    bokeh serve my_app_dir/\n\nIf this is not the case, renaming main.py will suppress this warning.\n'

@patch('warnings.warn')
def test_build_single_handler_application_main_py(mock_warn) -> None:
    f = tempfile.NamedTemporaryFile(suffix='main.py', delete=False)
    f.close()
    util.build_single_handler_application(f.name)
    assert mock_warn.called
    assert mock_warn.call_args[0] == (DIRSTYLE_MAIN_WARNING_COPY,)
    os.remove(f.name)
_SIZE_WARNING = 'Width/height arguments will be ignored for this muliple layout. (Size valus only apply when exporting single plots.)'

def Test_set_single_plot_width_height_test_neither(self) -> None:
    p = figure(plot_width=200, plot_height=300)
    d = Document()
    d.add_root(p)
    util.set_single_plot_width_height(d, None, None)
    assert p.plot_width == 200
    assert p.plot_height == 300

def Test_set_single_plot_width_height_test_width(self) -> None:
    p = figure(plot_width=200, plot_height=300)
    d = Document()
    d.add_root(p)
    util.set_single_plot_width_height(d, 400, None)
    assert p.plot_width == 400
    assert p.plot_height == 300

def Test_set_single_plot_width_height_test_height(self) -> None:
    p = figure(plot_width=200, plot_height=300)
    d = Document()
    d.add_root(p)
    util.set_single_plot_width_height(d, None, 400)
    assert p.plot_width == 200
    assert p.plot_height == 400

def Test_set_single_plot_width_height_test_both(self) -> None:
    p = figure(plot_width=200, plot_height=300)
    d = Document()
    d.add_root(p)
    util.set_single_plot_width_height(d, 400, 500)
    assert p.plot_width == 400
    assert p.plot_height == 500

def Test_set_single_plot_width_height_test_multiple_roots(self) -> None:
    p1 = figure(plot_width=200, plot_height=300)
    p2 = figure(plot_width=200, plot_height=300)
    d = Document()
    d.add_root(p1)
    d.add_root(p2)
    with pytest.warns(UserWarning) as warns:
        util.set_single_plot_width_height(d, 400, 500)
        assert len(warns) == 1
        assert warns[0].message.args[0] == _SIZE_WARNING

def Test_set_single_plot_width_height_test_layout(self) -> None:
    p = figure(plot_width=200, plot_height=300)
    d = Document()
    d.add_root(row(p))
    with pytest.warns(UserWarning) as warns:
        util.set_single_plot_width_height(d, 400, 500)
        assert len(warns) == 1
        assert warns[0].message.args[0] == _SIZE_WARNING