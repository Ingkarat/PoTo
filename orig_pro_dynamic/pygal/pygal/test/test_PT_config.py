from pygal.config import Key
from pygal.config import BaseConfig

def test_PT_is_boolean():
    k = Key()
    k.is_boolean()

def test_PT_is_numeric():
    k = Key()
    k.is_numeric()

def test_PT_is_string():
    k = Key()
    k.is_string()

def test_PT_is_dict():
    k = Key()
    k.is_dict()

def test_PT_is_list():
    k = Key()
    k.is_list()

def test_PT_coerce():
    k = Key()
    k.coerce(value)

def test_PT_to_dict():
    bc = BaseConfig()
    bc.to_dict()

def test_PT_copy():
    bc = BaseConfig()
    bc.copy()


