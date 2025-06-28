import pytest
pytest
from bokeh.models import FixedTicker, LinearAxis
import bokeh.models.grids as bmg

def test_ticker_accepts_number_sequences() -> None:
    g = bmg.Grid(ticker=[-10, 0, 10, 20.7])
    assert isinstance(g.ticker, FixedTicker)
    assert g.ticker.ticks == [-10, 0, 10, 20.7]
    g = bmg.Grid()
    g.ticker = [-10, 0, 10, 20.7]
    assert isinstance(g.ticker, FixedTicker)
    assert g.ticker.ticks == [-10, 0, 10, 20.7]

def test_ticker_accepts_axis() -> None:
    g = bmg.Grid(axis=LinearAxis())
    assert isinstance(g.axis, LinearAxis)
    g = bmg.Grid()
    g.axis = LinearAxis()
    assert isinstance(g.axis, LinearAxis)