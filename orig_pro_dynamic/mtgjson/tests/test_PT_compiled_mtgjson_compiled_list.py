from mtgjson.mtgjson5.compiled_classes.mtgjson_compiled_list import MtgjsonCompiledListObject

def test_PT_to_json():
    mf = MtgjsonCompiledListObject()
    mf.to_json()