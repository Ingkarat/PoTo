from mtgjson.mtgjson5.classes.mtgjson_deck import MtgjsonDeckObject

def test_PT_set_sanitized_name():
    md = MtgjsonDeckObject()
    md.set_sanitized_name("testname")

def test_PT_to_json():
    md = MtgjsonDeckObject()
    md.to_json()