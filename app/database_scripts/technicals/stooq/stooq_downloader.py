import os

import wget


class StooqDownloader:
    def __init__(self, url_base: str, url_end: str, save_dir: str):
        self.url_base = url_base
        self.url_end = url_end
        self.save_dir = save_dir
        self.fetched = 0
        # Stooq locks itself after ~200 downloads to prevent request floods.
        # If script returns blank files (blad.csv) then wait 24h and rerun.
        self.fetch_limit = 200

    def fetch_all(self, tickers: [str], to_download: int):
        tickers = [ticker.lower() for ticker in tickers]
        os.makedirs(self.save_dir, exist_ok=True)

        tickers = self.delete_ticker_if_data_exists(tickers)

        selected_tickers = zip(tickers, range(to_download))
        for ticker, i in selected_tickers:
            self.fetch_one(ticker)
            print(f"Downloaded {ticker} [{i + 1}/{to_download}]")

    def fetch_one(self, ticker: str):
        if self.fetched > self.fetch_limit:
            raise Exception("Too may fetches in one run")
        url = f"{self.url_base}{ticker}{self.url_end}"
        wget.download(url, out=self.save_dir)
        self.fetched += 1

    def delete_ticker_if_data_exists(self, tickers: [str]) -> [str]:
        return [
            ticker
            for ticker in tickers
            if not os.path.isfile(f"{self.save_dir}/{ticker}_d.csv")
        ]
