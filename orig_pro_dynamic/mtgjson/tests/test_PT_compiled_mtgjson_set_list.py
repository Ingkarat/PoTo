from mtgjson.mtgjson5.compiled_classes.mtgjson_set_list import MtgjsonSetListObject

def test_PT_get_all_set_list():
    mf = MtgjsonSetListObject()
    mf.get_all_set_list(["testfile"])

def test_PT_to_json():
    mf = MtgjsonSetListObject()
    mf.to_json()
