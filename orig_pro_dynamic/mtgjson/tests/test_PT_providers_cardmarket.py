import pathlib

from mtgjson.mtgjson5.providers.cardmarket import CardMarketProvider

def test_PT_generate_today_price_dict():
    cm = CardMarketProvider()
    p = pathlib.Path('/testpath')
    cm.generate_today_price_dict(p)

def test_PT_get_set_id():
    cm = CardMarketProvider()
    cm.get_set_id("teststr")

def test_PT_get_extras_set_id():
    cm = CardMarketProvider()
    cm.get_extras_set_id("testname")

def test_PT_get_set_name():
    cm = CardMarketProvider()
    cm.get_set_name("teststr")

def test_PT_download():
    cm = CardMarketProvider()
    cm.download("testurl",{"a","b"})

def test_PT_get_mkm_cards():
    cm = CardMarketProvider()
    cm2 = CardMarketProvider()
    cm.get_mkm_cards(1)
    cm2.get_mkm_cards(None)