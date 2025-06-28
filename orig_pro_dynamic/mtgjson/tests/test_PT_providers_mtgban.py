import pathlib

from mtgjson.mtgjson5.providers.mtgban import MTGBanProvider

def test_PT_download():
    gh = MTGBanProvider()
    url = "testurl"
    p = {"s":1}
    gh.download(url,p)

def test_PT_get_mtgjson_to_card_kingdom():
    gh = MTGBanProvider()
    gh.get_mtgjson_to_card_kingdom()