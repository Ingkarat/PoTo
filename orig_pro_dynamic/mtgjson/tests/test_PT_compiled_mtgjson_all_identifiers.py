from mtgjson.mtgjson5.compiled_classes.mtgjson_all_identifiers import MtgjsonAllIdentifiersObject

def test_PT_to_json():
    mf = MtgjsonAllIdentifiersObject()
    mf.to_json()
