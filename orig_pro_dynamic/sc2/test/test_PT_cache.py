from sc2.cache import cache_forever
from sc2.cache import property_cache_forever

def test_PT_cache_forever():
    cache_forever(f)

def test_PT_property_cache_forever():
    property_cache_forever(f)
    
def test_PT_property_cache_once_per_frame():
    property_cache_once_per_frame(f)

def test_PT_property_immutable_cache():
    property_immutable_cache(f)

def test_PT_property_mutable_cache():
    property_mutable_cache(f)