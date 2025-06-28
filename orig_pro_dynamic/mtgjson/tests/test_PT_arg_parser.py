from mtgjson.mtgjson5.arg_parser import parse_args
from mtgjson.mtgjson5.arg_parser import get_sets_already_built
from mtgjson.mtgjson5.arg_parser import get_all_scryfall_sets
from mtgjson.mtgjson5.arg_parser import get_sets_to_build



def test_PT_parse_args():
    parse_args()

def test_PT_get_sets_already_built():
    get_sets_already_built()

def test_PT_get_all_scryfall_sets():
    get_all_scryfall_sets()

def test_PT_get_sets_to_build():
    get_sets_to_build()