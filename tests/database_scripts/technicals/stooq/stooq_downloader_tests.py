import shutil

from app.database_scripts.technicals.stooq.stooq_downloader import StooqDownloader


def test_fetch_all_validTickers_shouldSaveAllFiles():
    url_base = "https://stooq.pl/q/d/l/?s="
    url_end = "&i=d"
    tickers = ["AST", "ATC"]
    database_dir = "./temp_db"
    downloader = StooqDownloader(url_base, url_end, database_dir)
    to_fetch = len(tickers)

    downloader.fetch_all(tickers, to_fetch)

    assert downloader.fetched == to_fetch

    shutil.rmtree("./temp_db")


def test_fetch_one_validTicker_shouldSaveOneFile():
    one_ticker = "pko"
    url_base = "https://stooq.pl/q/d/l/?s="
    url_end = "&i=d"
    database_dir = "./temp_db"
    downloader = StooqDownloader(url_base, url_end, database_dir)

    downloader.fetch_one(one_ticker)

    assert downloader.fetched == 1

    shutil.rmtree("./temp_db")


def test_delete_ticker_if_data_exists_ValidTickers_ShouldDeleteSomeTickersToDownload():
    database_dir = "./temp_db"
    fake_tickers = ["abc", "def"]

    downloader = StooqDownloader("", "", database_dir)
    f = open(f"{database_dir}/{fake_tickers[1]}_d.csv", "w")
    f.close()
    trimmed_tickers = downloader.delete_ticker_if_data_exists(fake_tickers)

    assert trimmed_tickers == ["abc"]

    shutil.rmtree("./temp_db")
