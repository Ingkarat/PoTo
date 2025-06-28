from mtgjson.mtgjson5.compiled_classes.mtgjson_all_printings import MtgjsonAllPrintingsObject

def test_PT_to_json():
    mf = MtgjsonAllPrintingsObject()
    mf.to_json()
