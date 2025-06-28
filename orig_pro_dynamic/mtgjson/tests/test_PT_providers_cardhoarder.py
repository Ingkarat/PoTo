import pathlib

from mtgjson.mtgjson5.providers.cardhoarder import CardHoarderProvider

def test_PT_download():
    ch = CardHoarderProvider()
    url = "testurl"
    p = {"s":1}
    ch.download(url,p)

def test_PT_convert_cardhoarder_to_mtgjson():
    ch = CardHoarderProvider()
    url = "testurl"
    m = {"a":"b"}
    ch.convert_cardhoarder_to_mtgjson(url,m)

def test_PT_generate_today_price_dict():
    ch = CardHoarderProvider()
    ch.generate_today_price_dict(a)

def test_PT_get_mtgo_to_mtgjson_map():
    ch = CardHoarderProvider()
    p = pathlib.Path('/testpath')
    ch.get_mtgo_to_mtgjson_map(p)
