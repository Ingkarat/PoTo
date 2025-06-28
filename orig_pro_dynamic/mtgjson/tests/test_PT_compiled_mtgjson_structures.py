from mtgjson.mtgjson5.compiled_classes.mtgjson_structures import MtgjsonStructuresObject

def test_PT_get_all_compiled_file_names():
    mf = MtgjsonStructuresObject()
    mf.get_all_compiled_file_names()

def test_PT_get_compiled_list_files():
    mf = MtgjsonStructuresObject()
    mf.get_compiled_list_files()

def test_PT_to_json():
    mf = MtgjsonStructuresObject()
    mf.to_json()


test_PT_compiled_mtgjson_structures