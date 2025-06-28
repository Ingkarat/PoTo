import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('numberly', 'probly')
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.perceptions', ALL))

@pytest.mark.sampledata
def test_numberly(pd) -> None:
    import bokeh.sampledata.perceptions as bsp
    assert isinstance(bsp.numberly, pd.DataFrame)
    assert len(bsp.numberly) == 46

@pytest.mark.sampledata
def test_probly(pd) -> None:
    import bokeh.sampledata.perceptions as bsp
    assert isinstance(bsp.probly, pd.DataFrame)
    assert len(bsp.probly) == 46