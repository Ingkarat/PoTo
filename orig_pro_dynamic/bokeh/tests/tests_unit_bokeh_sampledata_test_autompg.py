import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('autompg', 'autompg_clean')
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.autompg', ALL))

@pytest.mark.sampledata
def test_autompg(pd) -> None:
    import bokeh.sampledata.autompg as bsa
    assert isinstance(bsa.autompg, pd.DataFrame)
    assert len(bsa.autompg) == 392
    assert all((x in [1, 2, 3] for x in bsa.autompg.origin))

@pytest.mark.sampledata
def test_autompg_clean(pd) -> None:
    import bokeh.sampledata.autompg as bsa
    assert isinstance(bsa.autompg_clean, pd.DataFrame)
    assert len(bsa.autompg_clean) == 392
    assert all((x in ['North America', 'Europe', 'Asia'] for x in bsa.autompg_clean.origin))
    for x in ['chevy', 'chevroelt', 'maxda', 'mercedes-benz', 'toyouta', 'vokswagen', 'vw']:
        assert x not in bsa.autompg_clean.mfr