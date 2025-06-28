import pytest
pytest
from bokeh.document import Document
from bokeh.io.state import curstate
import bokeh.io.doc as bid

def test_curdoc_from_curstate() -> None:
    assert bid.curdoc() is curstate().document

def test_set_curdoc_sets_curstate() -> None:
    d = Document()
    bid.set_curdoc(d)
    assert curstate().document is d