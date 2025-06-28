import pathlib

from mtgjson.mtgjson5.providers.gatherer import GathererProvider

def test_PT_download():
    ch = GathererProvider()
    url = "testurl"
    p = {"s":1}
    ch.download(url,p)

def test_PT_get_cards():
    ch = GathererProvider()
    ch.get_cards("teststr","str")

def test_PT_parse_cards():
    ch = GathererProvider()
    ch.parse_cards("teststr",False)

def test_PT_strip_parentheses_from_text():
    ch = GathererProvider()
    ch.strip_parentheses_from_text("teststr")