import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('data',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.unemployment1948', ALL))

@pytest.mark.sampledata
def test_data(pd) -> None:
    import bokeh.sampledata.unemployment1948 as bsu
    assert isinstance(bsu.data, pd.DataFrame)
    assert len(bsu.data) == 69