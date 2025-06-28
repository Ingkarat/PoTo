from mtgjson.mtgjson5.classes.mtgjson_deck_header import MtgjsonDeckHeaderObject

def test_PT_to_json():
    md = MtgjsonDeckHeaderObject()
    md.to_json()
