import pathlib

from mtgjson.mtgjson5.providers.scryfall import ScryfallProvider

def test_PT_download():
    gh = ScryfallProvider()
    url = "testurl"
    p = {"s":1}
    gh.download(url,p)

def test_PT_download_cards():
    gh = ScryfallProvider()
    gh.download_cards("teststr")

def test_PT_generate_cards_without_limits():
    gh = ScryfallProvider()
    gh.generate_cards_without_limits()

def test_PT_get_catalog_entry():
    gh = ScryfallProvider()
    gh.get_catalog_entry("teststr")