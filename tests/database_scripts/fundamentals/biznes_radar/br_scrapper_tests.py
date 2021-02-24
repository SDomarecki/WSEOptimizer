import pandas as pd

from app.database_scripts.fundamentals.biznes_radar.br_scraper import BRScraper


def test_get_raw_fundamentals_validURL_shouldReturnFundamentals():
    br = BRScraper()
    link = '/KGHM'

    fundamentals: pd.DataFrame = br.get_raw_fundamentals(link)
    print(fundamentals)
    assert isinstance(fundamentals, pd.DataFrame)


def test_get_balance_validURL_shouldReturnBalance():
    br = BRScraper()
    link = '/KGHM'

    fundamentals: pd.DataFrame = br.get_balance(link)
    print(fundamentals)
    assert isinstance(fundamentals, pd.DataFrame)


def test_get_value_indicators_validURL_shouldReturnValueIndicators():
    br = BRScraper()
    link = '/KGHM'

    fundamentals: pd.DataFrame = br.get_value_indicators(link)
    print(fundamentals)
    assert isinstance(fundamentals, pd.DataFrame)


def test_get_profitability_indicators_validURL_shouldReturnProfitabilityIndicators():
    br = BRScraper()
    link = '/KGHM'

    fundamentals: pd.DataFrame = br.get_profitability_indicators(link)
    print(fundamentals)
    assert isinstance(fundamentals, pd.DataFrame)
