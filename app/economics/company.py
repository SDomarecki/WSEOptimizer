import pandas as pd


class Company:
    def __init__(self, name: str, ticker: str, link: str):
        self.name = name
        self.ticker = ticker
        self.link = link
        self.sector = ""
        self.fundamentals: pd.DataFrame
        self.technicals: pd.DataFrame
