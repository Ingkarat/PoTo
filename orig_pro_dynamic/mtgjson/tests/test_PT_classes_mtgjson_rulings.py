from mtgjson.mtgjson5.classes.mtgjson_rulings import MtgjsonRulingObject

def test_PT_to_json():
    mf = MtgjsonRulingObject()
    mf.to_json()