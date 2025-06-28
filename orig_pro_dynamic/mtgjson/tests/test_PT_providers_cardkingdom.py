import pathlib

from mtgjson.mtgjson5.providers.cardkingdom import CardKingdomProvider

def test_PT_download():
    ch = CardKingdomProvider()
    url = "testurl"
    p = {"s":1}
    ch.download(url,p)

def test_PT_generate_today_price_dict():
    ch = CardKingdomProvider()
    p = pathlib.Path('/testpath')
    ch.generate_today_price_dict(p)