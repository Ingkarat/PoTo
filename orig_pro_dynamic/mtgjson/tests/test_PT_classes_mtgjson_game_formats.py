from mtgjson.mtgjson5.classes.mtgjson_game_formats import MtgjsonGameFormatsObject

def test_PT_to_json():
    mf = MtgjsonGameFormatsObject()
    mf.to_json()