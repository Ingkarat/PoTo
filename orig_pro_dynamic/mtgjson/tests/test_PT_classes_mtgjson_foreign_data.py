from mtgjson.mtgjson5.classes.mtgjson_foreign_data import MtgjsonForeignDataObject

def test_PT_to_json():
    mf = MtgjsonForeignDataObject()
    mf.to_json()