import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('obiszow_mtb_xcm',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.mtb', ALL))

@pytest.mark.sampledata
def test_obiszow_mtb_xcm(pd) -> None:
    import bokeh.sampledata.mtb as bsm
    assert isinstance(bsm.obiszow_mtb_xcm, pd.DataFrame)
    assert len(bsm.obiszow_mtb_xcm) == 978