import pathlib

from mtgjson.mtgjson5.providers.github_decks import GitHubDecksProvider
from mtgjson.mtgjson5.providers.github_decks import build_single_card

def test_PT_download():
    gh = GitHubDecksProvider()
    url = "testurl"
    p = {"s":1}
    gh.download(url,p)

def test_PT_iterate_precon_decks():
    gh = GitHubDecksProvider()
    gh.iterate_precon_decks()
    
def test_PT_build_single_card():
    build_single_card({"a","b"})
    