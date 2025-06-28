import pathlib

from mtgjson.mtgjson5.providers.github_mtgsqlite import GitHubMTGSqliteProvider

def test_PT_download():
    gh = GitHubMTGSqliteProvider()
    url = "testurl"
    p = {"s":1}
    gh.download(url,p)

def test_PT_build_sql_and_csv_files():
    gh = GitHubMTGSqliteProvider()
    gh.build_sql_and_csv_files(url,p)
