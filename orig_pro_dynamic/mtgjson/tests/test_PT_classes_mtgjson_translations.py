from mtgjson.mtgjson5.classes.mtgjson_translations import MtgjsonTranslationsObject

def test_PT_parse_key():
    mf = MtgjsonTranslationsObject()
    mf.parse_key("teststr")

def test_PT_to_json():
    mf = MtgjsonTranslationsObject()
    mf.to_json()
