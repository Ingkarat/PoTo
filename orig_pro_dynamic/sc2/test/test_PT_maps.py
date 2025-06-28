from sc2.maps import get
from sc2.maps import Map

def test_PT_get():
    get()

def test_PT_name():
    m = Map()
    m.name()

def test_PT_data():
    m = Map()
    m.data()

def test_PT_matches():
    m = Map()
    m.matches()