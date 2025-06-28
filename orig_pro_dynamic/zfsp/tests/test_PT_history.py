from zfsp.zfs.history import next_break_offset
from zfsp.zfs.history import HistoryParser

def test_PT_next_break_offset():
    next_break_offset(5)

def test_PT_unpack_int():
    hp = HistoryParser()
    hp.unpack_int()

def test_PT_unpack_uint():
    hp = HistoryParser()
    hp.unpack_uint()

def test_PT_unpack_hyper():
    hp = HistoryParser()
    hp.unpack_hyper()

def test_PT_unpack_uhyper():
    hp = HistoryParser()
    hp.unpack_uhyper()

def test_PT_unpack_fstring():
    hp = HistoryParser()
    hp.unpack_fstring(5)

def test_PT_unpack_string():
    hp = HistoryParser()
    hp.unpack_string()

def test_PT_unpack_value():
    hp = HistoryParser()
    hp.unpack_value()

def test_PT_unpack_nvlist():
    hp = HistoryParser()
    hp.unpack_nvlist()

def test_PT_unpack_history():
    hp = HistoryParser()
    hp.unpack_history()