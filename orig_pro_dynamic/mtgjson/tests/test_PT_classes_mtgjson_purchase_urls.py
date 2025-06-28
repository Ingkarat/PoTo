from mtgjson.mtgjson5.classes.mtgjson_purchase_urls import MtgjsonPurchaseUrlsObject

def test_PT_build_keys_to_skip():
    mf = MtgjsonPurchaseUrlsObject()
    mf.build_keys_to_skip()

def test_PT_to_json():
    mf = MtgjsonPurchaseUrlsObject()
    mf.to_json()
