import pytest
pytest
import datetime as dt
import decimal
from collections import deque
import dateutil.relativedelta as rd
import numpy as np
from bokeh.colors import RGB
from bokeh.core.has_props import HasProps
from bokeh.core.properties import Int, String
from bokeh.models import Range1d

def TestBokehJSONEncoder_setup_method(self, test_method):
    from bokeh.core.json_encoder import BokehJSONEncoder
    self.encoder = BokehJSONEncoder()

def TestBokehJSONEncoder_test_fail(self) -> None:
    with pytest.raises(TypeError):
        BokehJSONEncoder().default({'testing': 1})

def TestBokehJSONEncoder_test_panda_series(self, pd) -> None:
    s = pd.Series([1, 3, 5, 6, 8])
    assert BokehJSONEncoder().default(s) == [1, 3, 5, 6, 8]

def TestBokehJSONEncoder_test_numpyarray(self) -> None:
    a = np.arange(5)
    assert BokehJSONEncoder().default(a) == [0, 1, 2, 3, 4]

def TestBokehJSONEncoder_test_numpyint(self) -> None:
    npint = np.asscalar(np.int64(1))
    assert BokehJSONEncoder().default(npint) == 1
    assert isinstance(BokehJSONEncoder().default(npint), int)

def TestBokehJSONEncoder_test_numpyfloat(self) -> None:
    npfloat = np.float64(1.33)
    assert BokehJSONEncoder().default(npfloat) == 1.33
    assert isinstance(BokehJSONEncoder().default(npfloat), float)

def TestBokehJSONEncoder_test_numpybool_(self) -> None:
    nptrue = np.bool_(True)
    assert BokehJSONEncoder().default(nptrue) == True
    assert isinstance(BokehJSONEncoder().default(nptrue), bool)

def TestBokehJSONEncoder_test_numpydatetime64(self) -> None:
    npdt64 = np.datetime64('2017-01-01')
    assert BokehJSONEncoder().default(npdt64) == 1483228800000.0
    assert isinstance(BokehJSONEncoder().default(npdt64), float)

def TestBokehJSONEncoder_test_time(self) -> None:
    dttime = dt.time(12, 32, 15)
    assert BokehJSONEncoder().default(dttime) == 45135000.0
    assert isinstance(BokehJSONEncoder().default(dttime), float)

def TestBokehJSONEncoder_test_relativedelta(self) -> None:
    rdelt = rd.relativedelta()
    assert isinstance(BokehJSONEncoder().default(rdelt), dict)

def TestBokehJSONEncoder_test_decimal(self) -> None:
    dec = decimal.Decimal(20.3)
    assert BokehJSONEncoder().default(dec) == 20.3
    assert isinstance(BokehJSONEncoder().default(dec), float)

def TestBokehJSONEncoder_test_model(self) -> None:
    m = Range1d(start=10, end=20)
    assert BokehJSONEncoder().default(m) == m.ref
    assert isinstance(BokehJSONEncoder().default(m), dict)

def TestBokehJSONEncoder_test_hasprops(self) -> None:
    hp = HP()
    assert BokehJSONEncoder().default(hp) == {}
    assert isinstance(BokehJSONEncoder().default(hp), dict)
    hp.foo = 15
    assert BokehJSONEncoder().default(hp) == {'foo': 15}
    assert isinstance(BokehJSONEncoder().default(hp), dict)
    hp.bar = 'test'
    assert BokehJSONEncoder().default(hp) == {'foo': 15, 'bar': 'test'}
    assert isinstance(BokehJSONEncoder().default(hp), dict)

def TestBokehJSONEncoder_test_color(self) -> None:
    c = RGB(16, 32, 64)
    assert BokehJSONEncoder().default(c) == 'rgb(16, 32, 64)'
    assert isinstance(BokehJSONEncoder().default(c), str)
    c = RGB(16, 32, 64, 0.1)
    assert BokehJSONEncoder().default(c) == 'rgba(16, 32, 64, 0.1)'
    assert isinstance(BokehJSONEncoder().default(c), str)

def TestBokehJSONEncoder_test_slice(self) -> None:
    c = slice(2)
    assert BokehJSONEncoder().default(c) == dict(start=None, stop=2, step=None)
    assert isinstance(BokehJSONEncoder().default(c), dict)
    c = slice(0, 2)
    assert BokehJSONEncoder().default(c) == dict(start=0, stop=2, step=None)
    assert isinstance(BokehJSONEncoder().default(c), dict)
    c = slice(0, 10, 2)
    assert BokehJSONEncoder().default(c) == dict(start=0, stop=10, step=2)
    assert isinstance(BokehJSONEncoder().default(c), dict)
    c = slice(0, None, 2)
    assert BokehJSONEncoder().default(c) == dict(start=0, stop=None, step=2)
    assert isinstance(BokehJSONEncoder().default(c), dict)
    c = slice(None, None, None)
    assert BokehJSONEncoder().default(c) == dict(start=None, stop=None, step=None)
    assert isinstance(BokehJSONEncoder().default(c), dict)

def TestBokehJSONEncoder_test_pd_timestamp(self, pd) -> None:
    ts = pd.Timestamp('April 28, 1948')
    assert BokehJSONEncoder().default(ts) == -684115200000

def TestSerializeJson_setup_method(self, test_method):
    from bokeh.core.json_encoder import serialize_json
    from json import loads
    self.serialize = serialize_json
    self.deserialize = loads

def TestSerializeJson_test_with_basic(self) -> None:
    assert serialize_json({'test': [1, 2, 3]}) == '{"test":[1,2,3]}'

def TestSerializeJson_test_pretty(self) -> None:
    assert serialize_json({'test': [1, 2, 3]}, pretty=True) == '{\n  "test": [\n    1,\n    2,\n    3\n  ]\n}'

def TestSerializeJson_test_with_np_array(self) -> None:
    a = np.arange(5)
    assert serialize_json(a) == '[0,1,2,3,4]'

def TestSerializeJson_test_with_pd_series(self, pd) -> None:
    s = pd.Series([0, 1, 2, 3, 4])
    assert serialize_json(s) == '[0,1,2,3,4]'

def TestSerializeJson_test_nans_and_infs(self) -> None:
    arr = np.array([np.nan, np.inf, -np.inf, 0])
    serialized = serialize_json(arr)
    deserialized = loads(serialized)
    assert deserialized[0] == 'NaN'
    assert deserialized[1] == 'Infinity'
    assert deserialized[2] == '-Infinity'
    assert deserialized[3] == 0

def TestSerializeJson_test_nans_and_infs_pandas(self, pd) -> None:
    arr = pd.Series(np.array([np.nan, np.inf, -np.inf, 0]))
    serialized = serialize_json(arr)
    deserialized = loads(serialized)
    assert deserialized[0] == 'NaN'
    assert deserialized[1] == 'Infinity'
    assert deserialized[2] == '-Infinity'
    assert deserialized[3] == 0

def TestSerializeJson_test_pandas_datetime_types(self, pd) -> None:
    """ should convert to millis """
    idx = pd.date_range('2001-1-1', '2001-1-5')
    df = pd.DataFrame({'vals': idx}, index=idx)
    serialized = serialize_json({'vals': df.vals, 'idx': df.index})
    deserialized = loads(serialized)
    baseline = {'vals': [978307200000, 978393600000, 978480000000, 978566400000, 978652800000], 'idx': [978307200000, 978393600000, 978480000000, 978566400000, 978652800000]}
    assert deserialized == baseline

def TestSerializeJson_test_builtin_datetime_types(self) -> None:
    """ should convert to millis as-is """
    DT_EPOCH = dt.datetime.utcfromtimestamp(0)
    a = dt.date(2016, 4, 28)
    b = dt.datetime(2016, 4, 28, 2, 20, 50)
    serialized = serialize_json({'a': [a], 'b': [b]})
    deserialized = loads(serialized)
    baseline = {'a': ['2016-04-28'], 'b': [(b - DT_EPOCH).total_seconds() * 1000.0 + b.microsecond / 1000.0]}
    assert deserialized == baseline
    assert deserialized == {'a': ['2016-04-28'], 'b': [1461810050000.0]}

def TestSerializeJson_test_builtin_timedelta_types(self) -> None:
    """ should convert time delta to a dictionary """
    delta = dt.timedelta(days=42, seconds=1138, microseconds=1337)
    serialized = serialize_json(delta)
    deserialized = loads(serialized)
    assert deserialized == delta.total_seconds() * 1000

def TestSerializeJson_test_numpy_timedelta_types(self) -> None:
    delta = np.timedelta64(3000, 'ms')
    serialized = serialize_json(delta)
    deserialized = loads(serialized)
    assert deserialized == 3000
    delta = np.timedelta64(3000, 's')
    serialized = serialize_json(delta)
    deserialized = loads(serialized)
    assert deserialized == 3000000

def TestSerializeJson_test_pandas_timedelta_types(self, pd) -> None:
    delta = pd.Timedelta('3000ms')
    serialized = serialize_json(delta)
    deserialized = loads(serialized)
    assert deserialized == 3000

def TestSerializeJson_test_deque(self) -> None:
    """Test that a deque is deserialized as a list."""
    assert serialize_json(deque([0, 1, 2])) == '[0,1,2]'

def TestSerializeJson_test_slice(self) -> None:
    """Test that a slice is deserialized as a list."""
    assert serialize_json(slice(2)) == '{"start":null,"step":null,"stop":2}'
    assert serialize_json(slice(0, 2)) == '{"start":0,"step":null,"stop":2}'
    assert serialize_json(slice(0, 10, 2)) == '{"start":0,"step":2,"stop":10}'
    assert serialize_json(slice(0, None, 2)) == '{"start":0,"step":2,"stop":null}'
    assert serialize_json(slice(None, None, None)) == '{"start":null,"step":null,"stop":null}'

def TestSerializeJson_test_bad_kwargs(self) -> None:
    with pytest.raises(ValueError):
        serialize_json([1], allow_nan=True)
    with pytest.raises(ValueError):
        serialize_json([1], separators=('a', 'b'))
    with pytest.raises(ValueError):
        serialize_json([1], sort_keys=False)