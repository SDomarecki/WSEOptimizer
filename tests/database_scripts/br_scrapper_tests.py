import pandas as pd

from app.database_scripts.br_scraper import BRscraper


def test_get_raw_fundamentals_validURL_shouldReturnFundamentals():
    br = BRscraper()
    link = '/KGHM'

    fundamentals: pd.DataFrame = br.get_raw_fundamentals(link)
    print(fundamentals)
    assert isinstance(fundamentals, pd.DataFrame)


def test_get_balance_validURL_shouldReturnBalance():
    br = BRscraper()
    link = '/KGHM'

    fundamentals: pd.DataFrame = br.get_balance(link)
    print(fundamentals)
    assert isinstance(fundamentals, pd.DataFrame)


def test_get_value_indicators_validURL_shouldReturnValueIndicators():
    br = BRscraper()
    link = '/KGHM'

    fundamentals: pd.DataFrame = br.get_value_indicators(link)
    print(fundamentals)
    assert isinstance(fundamentals, pd.DataFrame)


def test_get_profitability_indicators_validURL_shouldReturnProfitabilityIndicators():
    br = BRscraper()
    link = '/KGHM'

    fundamentals: pd.DataFrame = br.get_profitability_indicators(link)
    print(fundamentals)
    assert isinstance(fundamentals, pd.DataFrame)
