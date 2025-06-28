from mtgjson.mtgjson5.compiled_classes.mtgjson_keywords import MtgjsonKeywordsObject

def test_PT_to_json():
    mf = MtgjsonKeywordsObject()
    mf.to_json()