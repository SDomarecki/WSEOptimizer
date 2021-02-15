import shutil

import pytest

from app.database_scripts.stooq_download import StooqDownloader


@pytest.fixture(autouse=True, scope='package')
def create_and_destroy_database_directory():
    yield
    shutil.rmtree('tests')


def test_fetch_all_validTickers_shouldSaveAllFiles():
    url_base = 'https://stooq.pl/q/d/l/?s='
    url_end = '&i=d'
    tickers = ['AST', 'ATC', 'ATD', 'ATG', 'ATL', 'ATM']
    database_dir = 'tests/temp_db'
    downloader = StooqDownloader(tickers, url_base, url_end, database_dir)
    to_fetch = len(tickers)

    downloader.fetch_all(to_fetch)

    assert downloader.fetched == to_fetch


def test_fetch_one_validTicker_shouldSaveOneFile():
    one_ticker = 'pko'
    url_base = 'https://stooq.pl/q/d/l/?s='
    url_end = '&i=d'
    database_dir = 'tests/temp_db'
    downloader = StooqDownloader([], url_base, url_end, database_dir)

    downloader.fetch_one(one_ticker)

    assert downloader.fetched == 1


def test_delete_ticker_if_data_exists_ValidTickers_ShouldDeleteSomeTickersToDownload():
    database_dir = 'tests/temp_db'
    fake_tickers = ['abc', 'def']
    f = open(f'{database_dir}/{fake_tickers[1]}_d.csv', 'w')
    f.close()
    downloader = StooqDownloader(fake_tickers, '', '', database_dir)

    downloader.delete_ticker_if_data_exists()

    assert downloader.tickers == ['abc']
