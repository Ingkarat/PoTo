import pathlib

from mtgjson.mtgjson5.providers.tcgplayer import CardCondition
from mtgjson.mtgjson5.providers.tcgplayer import get_tcgplayer_sku_data
from mtgjson.mtgjson5.providers.tcgplayer import get_tcgplayer_sku_map
from mtgjson.mtgjson5.providers.tcgplayer import get_tcgplayer_buylist_prices_map
from mtgjson.mtgjson5.providers.tcgplayer import get_tcgplayer_prices_map
from mtgjson.mtgjson5.providers.tcgplayer import convert_sku_data_enum

def test_PT_download():
    gh = TCGPlayerProvider()
    url = "testurl"
    p = {"s":1}
    gh.download(url,p)

def test_PT_get_tcgplayer_magic_set_ids():
    gh = TCGPlayerProvider()
    gh.get_tcgplayer_magic_set_ids()

def test_PT_generate_today_price_dict():
    gh = TCGPlayerProvider()
    p = pathlib.Path('/testpath')
    gh.generate_today_price_dict(p)

def test_PT_get_tcgplayer_sku_data():
    get_tcgplayer_sku_data(("a","b"))

def test_PT_get_tcgplayer_sku_map():
    get_tcgplayer_sku_map([{"a":1}])

def test_PT_get_tcgplayer_buylist_prices_map():
    get_tcgplayer_buylist_prices_map(("a","b"),{"c":"d"})

def test_PT_get_tcgplayer_prices_map():
    get_tcgplayer_prices_map(("a","b"),{"c":"d"})

def test_PT_convert_sku_data_enum():
    convert_sku_data_enum({"a":1})