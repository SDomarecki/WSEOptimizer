import os

import pandas as pd
import pandas_ta as ta
from app.database_scripts.company_details import CompanyDetails
from app.database_scripts.technicals.stooq.stooq_downloader import StooqDownloader


class StooqPreprocessor:
    def __init__(self, database_path: str):
        stooq_base = "https://stooq.pl/q/d/l/?s="
        stooq_end = "&i=d"
        self.cache_dir = f"{database_path}/stooq"
        self.stooq_downloader = StooqDownloader(stooq_base, stooq_end, self.cache_dir)

    def fetch_technicals(self, company: CompanyDetails) -> pd.DataFrame:
        price_history = self.fetch_raw_history(company.ticker)
        return self.boost_technicals(price_history)

    def fetch_raw_history(self, ticker: str) -> pd.DataFrame:
        ticker = ticker.lower()
        if not os.path.isfile(f"{self.cache_dir}/{ticker}_d.csv"):
            self.stooq_downloader.fetch_one(ticker)
        price_history = pd.read_csv(f"{self.cache_dir}/{ticker}_d.csv", delimiter=",")
        return price_history

    def boost_technicals(self, technicals: pd.DataFrame) -> pd.DataFrame:
        technicals = self.change_column_names_from_polish_to_english(technicals)
        technicals = self.calculate_all_technicals_with_pandas_ta(technicals)
        technicals = self.set_date_as_index(technicals)
        return technicals

    @staticmethod
    def change_column_names_from_polish_to_english(
        technicals: pd.DataFrame,
    ) -> pd.DataFrame:
        new_columns = {
            "Data": "date",
            "Otwarcie": "open",
            "Najwyzszy": "high",
            "Najnizszy": "low",
            "Zamkniecie": "close",
            "Wolumen": "volume",
        }
        return technicals.rename(columns=new_columns)

    @staticmethod
    def calculate_all_technicals_with_pandas_ta(
        technicals: pd.DataFrame,
    ) -> pd.DataFrame:
        default_strategy = ta.Strategy(
            name="Default",
            description="PVOL, SMA15, SMA40, EMA200, RSI, MACD, Trix, Williams %R, MFI, ROC, EMV",
            ta=[
                {"kind": "pvol"},
                {"kind": "sma", "length": 15},
                {"kind": "sma", "length": 40},
                {"kind": "ema", "length": 200},
                {"kind": "rsi", "length": 14},
                {"kind": "macd", "fast": 12, "slow": 26, "signal": 9},
                {"kind": "trix", "length": 14, "signal": 9},
                {"kind": "willr", "length": 10},
                {"kind": "mfi", "length": 14},
                {"kind": "roc", "length": 14},
                {"kind": "eom", "length": 14},
            ],
        )

        technicals.ta.strategy(default_strategy)
        return technicals

    @staticmethod
    def set_date_as_index(technicals: pd.DataFrame) -> pd.DataFrame:
        return technicals.set_index("date")
