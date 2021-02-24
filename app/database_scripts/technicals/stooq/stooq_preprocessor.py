import os

import pandas as pd

import app.database_scripts.technicals.stooq.indicators as ind
from app.database_scripts.company_details import CompanyDetails
from app.database_scripts.technicals.stooq.stooq_downloader import StooqDownloader


class StooqPreprocessor:
    def __init__(self):
        stooq_base = 'https://stooq.pl/q/d/l/?s='
        stooq_end = '&i=d'
        self.cache_dir = 'database/stooq'
        self.stooq_downloader = StooqDownloader(stooq_base, stooq_end, self.cache_dir)

    def fetch_technicals(self, company: CompanyDetails) -> pd.DataFrame:
        price_history = self.fetch_raw_history(company.ticker)
        return self.boost_technicals(price_history)

    def fetch_raw_history(self, ticker: str) -> pd.DataFrame:
        ticker = ticker.lower()
        if not os.path.isfile(f'{self.cache_dir}/{ticker}_d.csv'):
            self.stooq_downloader.fetch_one(ticker)
        price_history = pd.read_csv(f'{self.cache_dir}/{ticker}_d.csv', delimiter=',')
        return price_history

    def boost_technicals(self, technicals: pd.DataFrame) -> pd.DataFrame:
        technicals = self.change_column_names_from_polish_to_english(technicals)
        technicals = self.calculate_all_technicals(technicals)
        technicals = self.set_date_as_index(technicals)
        return technicals

    def change_column_names_from_polish_to_english(self, technicals: pd.DataFrame) -> pd.DataFrame:
        new_columns = {'Data': 'Date',
                       'Otwarcie': 'Open',
                       'Najwyzszy': 'High',
                       'Najnizszy': 'Low',
                       'Zamkniecie': 'Close',
                       'Wolumen': 'Volume'}
        return technicals.rename(columns=new_columns)

    def calculate_all_technicals(self, technicals: pd.DataFrame) -> pd.DataFrame:
        t = technicals

        t = ind.circulation(t, close_col='Close', vol_col='Volume')
        t = ind.sma(t, period=15, close_col='Close')
        t = ind.sma(t, period=40, close_col='Close')
        t = ind.ema(t, period=200, close_col='Close')
        t = ind.rsi(t, periods=14, close_col='Close')
        t = ind.macd(t,
                     period_long=26,
                     period_short=12,
                     period_signal=9,
                     close_col='Close')
        t = ind.trix(t, periods=14, signal_periods=9, close_col='Close')
        t = ind.williams_r(t,
                           periods=10,
                           high_col='High',
                           low_col='Low',
                           close_col='Close')
        t = ind.money_flow_index(t,
                                 periods=14,
                                 high_col='High',
                                 low_col='Low',
                                 close_col='Close',
                                 vol_col='Volume')
        t = ind.roc(t, periods=14, close_col='Close')
        t = ind.ease_of_movement(t,
                                 period=14,
                                 high_col='High',
                                 low_col='Low',
                                 vol_col='Volume')

        return t

    def set_date_as_index(self, technicals: pd.DataFrame) -> pd.DataFrame:
        return technicals.set_index('Date')
