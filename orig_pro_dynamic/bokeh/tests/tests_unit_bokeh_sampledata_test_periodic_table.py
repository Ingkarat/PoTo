import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('elements',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.periodic_table', ALL))

@pytest.mark.sampledata
def test_elements(pd) -> None:
    import bokeh.sampledata.periodic_table as bsp
    assert isinstance(bsp.elements, pd.DataFrame)
    assert len(bsp.elements) == 118