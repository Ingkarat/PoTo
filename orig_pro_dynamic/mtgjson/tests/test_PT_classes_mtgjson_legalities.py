from mtgjson.mtgjson5.classes.mtgjson_legalities import MtgjsonLegalitiesObject

def test_PT_to_json():
    mf = MtgjsonLegalitiesObject()
    mf.to_json()
