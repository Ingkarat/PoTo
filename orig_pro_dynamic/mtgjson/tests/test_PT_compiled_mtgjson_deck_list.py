from mtgjson.mtgjson5.compiled_classes.mtgjson_deck_list import MtgjsonDeckListObject

def test_PT_to_json():
    mf = MtgjsonDeckListObject()
    mf.to_json()