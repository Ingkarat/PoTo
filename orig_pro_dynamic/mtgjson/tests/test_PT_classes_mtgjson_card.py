from mtgjson.mtgjson5.classes.mtgjson_card import MtgjsonCardObject

def test_PT_set_illustration_ids():
    mc = MtgjsonCardObject()
    mc.set_illustration_ids("teststr")
    
def test_PT_get_illustration_ids():
    mc = MtgjsonCardObject()
    mc.get_illustration_ids()
    
def test_PT_get_names():
    mc = MtgjsonCardObject()
    mc.get_names()
    
def test_PT_set_names():
    mc = MtgjsonCardObject()
    mc.set_names()
    
def test_PT_append_names():
    mc = MtgjsonCardObject()
    mc.append_names()
    
def test_PT_set_watermark():
    mc = MtgjsonCardObject()
    mc2 = MtgjsonCardObject()
    mc.set_watermark("water")
    mc2.set_watermark(None)
    
def test_PT_get_atomic_keys():
    mc = MtgjsonCardObject()
    mc.get_atomic_keys()
    
def test_PT_build_keys_to_skip():
    mc = MtgjsonCardObject()
    mc.build_keys_to_skip()
    
def test_PT_to_json():
    mc = MtgjsonCardObject()
    mc.to_json()
