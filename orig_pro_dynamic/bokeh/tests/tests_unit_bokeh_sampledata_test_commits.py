import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('data',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.commits', ALL))

@pytest.mark.sampledata
def test_data(pd) -> None:
    import bokeh.sampledata.commits as bsc
    assert isinstance(bsc.data, pd.DataFrame)
    assert len(bsc.data) == 4916