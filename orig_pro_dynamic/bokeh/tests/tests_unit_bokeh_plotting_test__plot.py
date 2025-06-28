import pytest
pytest
import datetime
import numpy as np
from bokeh.models import CategoricalAxis, CategoricalScale, DataRange1d, DatetimeAxis, FactorRange, LinearAxis, LinearScale, LogAxis, LogScale, MercatorAxis, Range1d
import bokeh.plotting._plot as bpp
_RANGES = [Range1d(), DataRange1d(), FactorRange()]

def test_get_scale_factor_range_test_numeric_range_linear_axis() -> None:
    s = bpp.get_scale(Range1d(), 'linear')
    assert isinstance(s, LinearScale)
    s = bpp.get_scale(Range1d(), 'datetime')
    assert isinstance(s, LinearScale)
    s = bpp.get_scale(Range1d(), 'auto')
    assert isinstance(s, LinearScale)

def test_get_scale_factor_range_test_numeric_range_log_axis() -> None:
    s = bpp.get_scale(DataRange1d(), 'log')
    assert isinstance(s, LogScale)

def test_get_scale_factor_range_test_factor_range() -> None:
    s = bpp.get_scale(FactorRange(), 'auto')
    assert isinstance(s, CategoricalScale)

def Test_get_range_test_with_None(self) -> None:
    r = bpp.get_range(None)
    assert isinstance(r, DataRange1d)

def Test_get_range_test_with_Range(self) -> None:
    for t in [Range1d, DataRange1d, FactorRange]:
        rng = t()
        r = bpp.get_range(rng)
        assert r is rng

def Test_get_range_test_with_ndarray(self) -> None:
    r = bpp.get_range(np.array([10, 20]))
    assert isinstance(r, Range1d)
    assert r.start == 10
    assert r.end == 20

def Test_get_range_test_with_too_long_ndarray(self) -> None:
    with pytest.raises(ValueError):
        bpp.get_range(np.array([10, 20, 30]))

def Test_get_range_test_with_ndarray_factors(self) -> None:
    f = np.array(['Crosby', 'Stills', 'Nash', 'Young'])
    r = bpp.get_range(f)
    assert isinstance(r, FactorRange)
    assert r.factors == list(f)

def Test_get_range_test_with_series(self, pd) -> None:
    r = bpp.get_range(pd.Series([20, 30]))
    assert isinstance(r, Range1d)
    assert r.start == 20
    assert r.end == 30

def Test_get_range_test_with_too_long_series(self, pd) -> None:
    with pytest.raises(ValueError):
        bpp.get_range(pd.Series([20, 30, 40]))

def Test_get_range_test_with_string_seq(self) -> None:
    f = ['foo', 'end', 'baz']
    for t in [list, tuple]:
        r = bpp.get_range(t(f))
        assert isinstance(r, FactorRange)
        assert r.factors == f

def Test_get_range_test_with_float_bounds(self) -> None:
    r = bpp.get_range((1.2, 10))
    assert isinstance(r, Range1d)
    assert r.start == 1.2
    assert r.end == 10
    r = bpp.get_range([1.2, 10])
    assert isinstance(r, Range1d)
    assert r.start == 1.2
    assert r.end == 10

def Test_get_range_test_with_pandas_group(self, pd) -> None:
    from bokeh.sampledata.iris import flowers
    g = flowers.groupby('species')
    r = bpp.get_range(g)
    assert isinstance(r, FactorRange)
    assert r.factors == ['setosa', 'versicolor', 'virginica']

@pytest.mark.parametrize('range', _RANGES)
def Test__get_axis_class_test_axis_type_None(self, range) -> None:
    range = _RANGES[0]
    assert bpp._get_axis_class(None, range, 0) == (None, {})
    assert bpp._get_axis_class(None, range, 1) == (None, {})

@pytest.mark.parametrize('range', _RANGES)
def Test__get_axis_class_test_axis_type_linear(self, range) -> None:
    range = _RANGES[0]
    assert bpp._get_axis_class('linear', range, 0) == (LinearAxis, {})
    assert bpp._get_axis_class('linear', range, 1) == (LinearAxis, {})

@pytest.mark.parametrize('range', _RANGES)
def Test__get_axis_class_test_axis_type_log(self, range) -> None:
    range = _RANGES[0]
    assert bpp._get_axis_class('log', range, 0) == (LogAxis, {})
    assert bpp._get_axis_class('log', range, 1) == (LogAxis, {})

@pytest.mark.parametrize('range', _RANGES)
def Test__get_axis_class_test_axis_type_datetime(self, range) -> None:
    range = _RANGES[0]
    assert bpp._get_axis_class('datetime', range, 0) == (DatetimeAxis, {})
    assert bpp._get_axis_class('datetime', range, 1) == (DatetimeAxis, {})

@pytest.mark.parametrize('range', _RANGES)
def Test__get_axis_class_test_axis_type_mercator(self, range) -> None:
    range = _RANGES[0]
    assert bpp._get_axis_class('mercator', range, 0) == (MercatorAxis, {'dimension': 'lon'})
    assert bpp._get_axis_class('mercator', range, 1) == (MercatorAxis, {'dimension': 'lat'})

def Test__get_axis_class_test_axis_type_auto(self) -> None:
    assert bpp._get_axis_class('auto', FactorRange(), 0) == (CategoricalAxis, {})
    assert bpp._get_axis_class('auto', FactorRange(), 1) == (CategoricalAxis, {})
    assert bpp._get_axis_class('auto', DataRange1d(), 0) == (LinearAxis, {})
    assert bpp._get_axis_class('auto', DataRange1d(), 1) == (LinearAxis, {})
    assert bpp._get_axis_class('auto', Range1d(), 0) == (LinearAxis, {})
    assert bpp._get_axis_class('auto', Range1d(), 1) == (LinearAxis, {})
    assert bpp._get_axis_class('auto', Range1d(start=datetime.datetime(2018, 3, 21)), 0) == (DatetimeAxis, {})
    assert bpp._get_axis_class('auto', Range1d(start=datetime.datetime(2018, 3, 21)), 1) == (DatetimeAxis, {})

@pytest.mark.parametrize('range', _RANGES)
def Test__get_axis_class_test_axis_type_error(self, range) -> None:
    range = _RANGES[0]
    with pytest.raises(ValueError):
        bpp._get_axis_class('junk', range, 0)
    with pytest.raises(ValueError):
        bpp._get_axis_class('junk', range, 1)