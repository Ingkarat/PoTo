import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('sprint',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.sprint', ALL))

@pytest.mark.sampledata
def test_sprint(pd) -> None:
    import bokeh.sampledata.sprint as bss
    assert isinstance(bss.sprint, pd.DataFrame)
    assert len(bss.sprint) == 85