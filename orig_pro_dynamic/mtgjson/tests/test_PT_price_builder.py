import configParser

from mtgjson.mtgjson5.price_builder import download_prices_archive
from mtgjson.mtgjson5.price_builder import upload_prices_archive
from mtgjson.mtgjson5.price_builder import prune_prices_archive
from mtgjson.mtgjson5.price_builder import build_today_prices
from mtgjson.mtgjson5.price_builder import get_price_archive_data
from mtgjson.mtgjson5.price_builder import download_old_all_printings
from mtgjson.mtgjson5.price_builder import build_prices
from mtgjson.mtgjson5.price_builder import should_build_new_prices

def test_PT_download_prices_archive():
    c = configparser.ConfigParser()
    p = pathlib.Path('/testpath')
    download_prices_archive(c,p)
    
def test_PT_upload_prices_archive():
    c = configparser.ConfigParser()
    p = pathlib.Path('/testpath')
    upload_prices_archive(c,p,content)
    
def test_PT_prune_prices_archive():
    c = {"text":"test"}
    m = 3
    prune_prices_archive(c,m)
    
def test_PT_build_today_prices():
    build_today_prices()
    
def test_PT_get_price_archive_data():
    get_price_archive_data()
    
def test_PT_download_old_all_printings():
    download_old_all_printings()
    
def test_PT_build_prices():
    build_prices()
    
def test_PT_should_build_new_prices():
    should_build_new_prices()