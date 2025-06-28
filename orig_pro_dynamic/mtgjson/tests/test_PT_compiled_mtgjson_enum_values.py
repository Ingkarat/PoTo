from mtgjson.mtgjson5.compiled_classes.mtgjson_enum_values import MtgjsonEnumValuesObject

def test_PT_construct_deck_enums():
    mf = MtgjsonEnumValuesObject()
    p = pathlib.Path('/testpath')
    mf.construct_deck_enums(p)
    
def test_PT_construct_set_and_card_enums():
    mf = MtgjsonEnumValuesObject()
    mf.construct_set_and_card_enums({"a",1})
    
def test_PT_to_json():
    mf = MtgjsonEnumValuesObject()
    mf.to_json()
