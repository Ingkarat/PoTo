from typing import Match

from mtgjson.mtgjson5.compiled_classes.mtgjson_card_types import MtgjsonCardTypesObject
from mtgjson.mtgjson5.compiled_classes.mtgjson_card_types import regex_str_to_list

def test_PT_to_json():
    mf = MtgjsonCardTypesObject()
    mf.to_json()

def test_PT_regex_str_to_list():
    regex_str_to_list(None)
    regex_str_to_list(Match)