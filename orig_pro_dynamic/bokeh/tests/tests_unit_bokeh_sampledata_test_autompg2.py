import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('autompg2',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.autompg2', ALL))

@pytest.mark.sampledata
def test_autompg2(pd) -> None:
    import bokeh.sampledata.autompg2 as bsa
    assert isinstance(bsa.autompg2, pd.DataFrame)
    assert len(bsa.autompg2) == 234