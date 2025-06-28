from mtgjson.mtgjson5.classes.mtgjson_identifiers import MtgjsonIdentifiersObject

def test_PT_to_json():
    mf = MtgjsonIdentifiersObject()
    mf.to_json()
