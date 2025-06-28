from mtgjson.mtgjson5.classes.mtgjson_prices import MtgjsonPricesObject

def test_PT_to_json():
    mf = MtgjsonPricesObject()
    mf.to_json()