import pandas as pd


class Company:
    def __init__(self, name: str, ticker: str, link: str, sector: str):
        self.name = name
        self.ticker = ticker
        self.link = link
        self.sector = sector
        self.fundamentals: pd.DataFrame
        self.technicals: pd.DataFrame
