from mtgjson.mtgjson5.referral_builder import build_and_write_referral_map
from mtgjson.mtgjson5.referral_builder import build_referral_map
from mtgjson.mtgjson5.referral_builder import write_referral_map
from mtgjson.mtgjson5.referral_builder import fixup_referral_map
from mtgjson.mtgjson5.classes import MtgjsonSetObject

def test_PT_build_and_write_referral_map():
    ms = MtgjsonSetObject()
    build_and_write_referral_map(ms)

def test_PT_build_referral_map():
    ms = MtgjsonSetObject()
    build_referral_map(ms)

def test_PT_write_referral_map():
    l = [("a","b")]
    write_referral_map(l)

def test_PT_fixup_referral_map():
    fixup_referral_map()
