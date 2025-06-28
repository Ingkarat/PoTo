import pytest
pytest
import bokeh.io.notebook as binb
from bokeh._testing.util.api import verify_all
import bokeh.io as bi
ALL = ('curdoc', 'export_png', 'export_svgs', 'install_notebook_hook', 'push_notebook', 'output_file', 'output_notebook', 'save', 'show')
Test___all__ = verify_all(bi, ALL)

def test_jupyter_notebook_hook_installed() -> None:
    assert list(binb._HOOKS) == ['jupyter']
    assert binb._HOOKS['jupyter']['load'] == binb.load_notebook
    assert binb._HOOKS['jupyter']['doc'] == binb.show_doc
    assert binb._HOOKS['jupyter']['app'] == binb.show_app