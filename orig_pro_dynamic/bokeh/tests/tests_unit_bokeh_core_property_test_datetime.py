import pytest
pytest
import datetime
import numpy as np
from _util_property import _TestHasProps, _TestModel
from bokeh._testing.util.api import verify_all
from bokeh.util.serialization import convert_date_to_datetime
import bokeh.core.property.datetime as bcpd
ALL = ('Date', 'Datetime', 'TimeDelta')
Test___all__ = verify_all(bcpd, ALL)

def Test_Date_test_valid(self) -> None:
    prop = bcpd.Date()
    assert prop.is_valid(datetime.date(2020, 1, 11))
    assert prop.is_valid('2020-01-10')
    assert prop.is_valid(None)

def Test_Date_test_invalid(self) -> None:
    prop = bcpd.Date()
    assert not prop.is_valid(datetime.datetime(2020, 1, 11))
    assert not prop.is_valid('')
    assert not prop.is_valid(False)
    assert not prop.is_valid(True)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())

def Test_Date_test_has_ref(self) -> None:
    prop = bcpd.Date()
    assert not prop.has_ref

def Test_Date_test_str(self) -> None:
    prop = bcpd.Date()
    assert str(prop) == 'Date'

def Test_Datetime_test_valid(self, pd) -> None:
    prop = bcpd.Datetime()
    assert prop.is_valid(None)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid(0.0)
    assert prop.is_valid(1.0)
    assert prop.is_valid('2020-01-11T13:00:00')
    assert prop.is_valid(datetime.datetime.now())
    assert prop.is_valid(datetime.time(10, 12))
    assert prop.is_valid(np.datetime64('2020-01-11'))
    if pd:
        assert prop.is_valid(pd.Timestamp('2010-01-11'))

def Test_Datetime_test_invalid(self) -> None:
    prop = bcpd.Datetime()
    assert not prop.is_valid('')
    assert not prop.is_valid(False)
    assert not prop.is_valid(True)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())

def Test_Datetime_test_is_timestamp(self) -> None:
    assert bcpd.Datetime.is_timestamp(0)
    assert bcpd.Datetime.is_timestamp(0.0)
    assert bcpd.Datetime.is_timestamp(10)
    assert bcpd.Datetime.is_timestamp(10.0)
    assert bcpd.Datetime.is_timestamp(-10)
    assert bcpd.Datetime.is_timestamp(-10)
    assert bcpd.Datetime.is_timestamp(-10.0)
    assert not bcpd.Datetime.is_timestamp(True)
    assert not bcpd.Datetime.is_timestamp(False)

def Test_Datetime_test_transform_date(self) -> None:
    t = datetime.date(2020, 1, 11)
    prop = bcpd.Datetime()
    assert prop.transform(t) == convert_date_to_datetime(t)

def Test_Datetime_test_transform_str(self) -> None:
    t = datetime.date(2020, 1, 11)
    prop = bcpd.Datetime()
    assert prop.transform('2020-01-11') == convert_date_to_datetime(t)

def Test_Datetime_test_has_ref(self) -> None:
    prop = bcpd.Datetime()
    assert not prop.has_ref

def Test_Datetime_test_str(self) -> None:
    prop = bcpd.Datetime()
    assert str(prop) == 'Datetime'