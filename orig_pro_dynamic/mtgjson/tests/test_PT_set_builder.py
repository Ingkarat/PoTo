from mtgjson.mtgjson5.set_builder import build_and_write_referral_map
from mtgjson.mtgjson5.set_builder import parse_card_types
from mtgjson.mtgjson5.set_builder import get_card_colors
from mtgjson.mtgjson5.set_builder import get_scryfall_set_data
from mtgjson.mtgjson5.set_builder import is_number
from mtgjson.mtgjson5.set_builder import get_card_cmc
from mtgjson.mtgjson5.set_builder import parse_printings
from mtgjson.mtgjson5.set_builder import parse_legalities
from mtgjson.mtgjson5.set_builder import parse_rulings
from mtgjson.mtgjson5.set_builder import test_PT_relocate_miscellaneous_tokens
from mtgjson.mtgjson5.set_builder import mark_duel_decks
from mtgjson.mtgjson5.set_builder import parse_keyrune_code
from mtgjson.mtgjson5.set_builder import build_mtgjson_set
from mtgjson.mtgjson5.set_builder import build_base_mtgjson_tokens
from mtgjson.mtgjson5.set_builder import build_base_mtgjson_cards
from mtgjson.mtgjson5.set_builder import add_is_starter_option
from mtgjson.mtgjson5.set_builder import add_leadership_skills
from mtgjson.mtgjson5.set_builder import add_uuid
from mtgjson.mtgjson5.set_builder import build_mtgjson_card
from mtgjson.mtgjson5.set_builder import add_variations_and_alternative_fields
from mtgjson.mtgjson5.set_builder import add_mcm_details
from mtgjson.mtgjson5.set_builder import get_base_and_total_set_sizes

from mtgjson.mtgjson5.classes import MtgjsonSetObject
from mtgjson.mtgjson5.classes import MtgjsonCardObject

def test_PT_parse_foreign():
    parse_foreign("url","cardname","cardnum","setname")

def test_PT_parse_card_types():
    parse_card_types("cardtype")

def test_PT_get_card_colors():
    get_card_colors("manacost")

def test_PT_get_scryfall_set_data():
    get_scryfall_set_data("setcode")

def test_PT_is_number():
    is_number("teststr")

def test_PT_get_card_cmc():
    get_card_cmc("manacost")

def test_PT_parse_printings():
    parse_printings(None)
    parse_printings("testtext")

def test_PT_parse_legalities():
    d = {"a","b"}
    parse_legalities(d)

def test_PT_parse_rulings():
    parse_rulings("testurl")

def test_PT_relocate_miscellaneous_tokens():
    ms = MtgjsonSetObject()
    relocate_miscellaneous_tokens(ms)

def test_PT_mark_duel_decks():
    ms = MtgjsonSetObject() 
    cards = [ms]
    mark_duel_decks("setcode", cards)

def test_PT_parse_keyrune_code():
    parse_keyrune_code("testurl")

def test_PT_build_mtgjson_set():
    build_mtgjson_set("testcode")

def test_PT_build_base_mtgjson_tokens():
    s = "testcode"
    at = [{"a","b"}]
    build_base_mtgjson_tokens(s,at)

def test_PT_build_base_mtgjson_cards():
    s = "testcode"
    at = [{"a","b"}]
    build_base_mtgjson_cards(s,at,False,"")

def test_PT_add_is_starter_option():
    mc = MtgjsonCardObject() 
    cards = [mc]
    add_is_starter_option("setcode","url",cards)

def test_PT_add_leadership_skills():
    mc = MtgjsonCardObject() 
    add_leadership_skills(mc)

def test_PT_add_uuid():
    mc = MtgjsonCardObject() 
    add_uuid(mc)

def test_PT_build_mtgjson_card():
    build_mtgjson_card({"a","b"},0,False,"")

def test_PT_add_variations_and_alternative_fields():
    ms = MtgjsonSetObject()
    add_variations_and_alternative_fields(ms)

def test_PT_add_mcm_details():
    ms = MtgjsonSetObject()
    add_mcm_details(ms)

def test_PT_get_base_and_total_set_sizes():
    get_base_and_total_set_sizes("teststr")
