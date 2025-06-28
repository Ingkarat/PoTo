import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('data',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.degrees', ALL))

@pytest.mark.sampledata
def test_data(pd) -> None:
    import bokeh.sampledata.degrees as bsd
    assert isinstance(bsd.data, pd.DataFrame)
    assert len(bsd.data) == 42