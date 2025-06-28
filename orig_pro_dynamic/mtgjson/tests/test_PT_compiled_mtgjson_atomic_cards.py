from mtgjson.mtgjson5.compiled_classes.mtgjson_atomic_cards import MtgjsonAtomicCardsObject

def test_PT_iterate_all_cards():
    mf = MtgjsonAtomicCardsObject()
    l = ["file"]
    c = [{"a",1}]
    mf.iterate_all_cards(l,c)

def test_PT_update_global_card_list():
    mf = MtgjsonAtomicCardsObject()
    l = ["file"]
    c = [{"a",1}]
    mf.to_jupdate_global_card_listson(l,c)

def test_PT_to_json():
    mf = MtgjsonAtomicCardsObject()
    mf.to_json()

