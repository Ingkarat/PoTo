from mtgjson.mtgjson5.compiled_classes.mtgjson_tcgplayer_skus import MtgjsonTcgplayerSkusObject

def test_PT_to_json():
    mf = MtgjsonTcgplayerSkusObject()
    mf.to_json()