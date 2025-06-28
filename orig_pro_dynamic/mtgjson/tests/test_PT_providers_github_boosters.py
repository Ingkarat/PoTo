import pathlib

from mtgjson.mtgjson5.providers.github_boosters import GitHubBoostersProvider

def test_PT_download():
    gh = GitHubBoostersProvider()
    url = "testurl"
    p = {"s":1}
    gh.download(url,p)

def get_set_booster_data():
    gh = GitHubBoostersProvider()
    gh.get_set_booster_data("teststr")