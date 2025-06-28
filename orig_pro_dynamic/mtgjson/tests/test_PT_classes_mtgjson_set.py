from mtgjson.mtgjson5.classes.mtgjson_set import MtgjsonSetObject

def test_PT_build_keys_to_skip():
    mf = MtgjsonSetObject()
    mf.build_keys_to_skip()

def test_PT_to_json():
    mf = MtgjsonSetObject()
    mf.to_json()

