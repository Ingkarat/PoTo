from datetime import datetime,time,timedelta

from pygal.graph.time import datetime_to_timestamp
from pygal.graph.time import datetime_to_time
from pygal.graph.time import date_to_datetime
from pygal.graph.time import time_to_datetime
from pygal.graph.time import timedelta_to_seconds
from pygal.graph.time import time_to_seconds
from pygal.graph.time import seconds_to_time

def test_PT_datetime_to_timestamp():
    dt = datetime(1, 4, 24, 2)
    datetime_to_timestamp(dt)

def test_PT_datetime_to_time():
    dt = datetime(1, 4, 24, 2)
    datetime_to_time(dt)

def test_PT_date_to_datetime():
    dt = datetime(1, 4, 24, 2)
    date_to_datetime(dt)

def test_PT_time_to_datetime():
    t = time(12, 30)
    time_to_datetime(t)

def test_PT_timedelta_to_seconds():
    td = timedelta(days=365)
    timedelta_to_seconds(td)

def test_PT_time_to_seconds():
    t = time(12, 30)
    time_to_seconds(t)
    time_to_seconds("1")

def test_PT_seconds_to_time():
    seconds_to_time("1")
