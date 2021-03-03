from datetime import date

import pytest
import pandas as pd
from app.economics.company import Company


@pytest.fixture(scope="package")
def company() -> Company:
    company = Company("test", "TEST", "/test", "sector:test")
    fundamental_index = ["2000/Q1", "2000/Q2", "2000/Q3", "2000/Q4", "2001/Q1"]
    fundamental_data = {
        "P/BV": [1.0, 1.5, 2.0, 2.5, 3.0],
        "P/E": [1.0, 1.5, 2.0, 2.5, 3.0],
        "P/S": [1.0, 1.5, 2.0, 2.5, 3.0],
        "BVPS": [10.0, 10.0, 10.0, 10.0, 10.0],
        "EPS": [10.0, 10.0, 10.0, 10.0, 10.0],
        "SPS": [10.0, 10.0, 10.0, 10.0, 10.0],
        "ROA": [0.1, 0.2, 0.3, 0.4, 0.5],
        "ROE": [0.1, 0.2, 0.3, 0.4, 0.5],
    }
    company.fundamentals = pd.DataFrame(fundamental_data, index=fundamental_index)
    technical_index = [date(2000, 6, 1), date(2001, 1, 1), date(2001, 6, 1)]
    technical_data = {
        "close": [10.0, 20.0, 30.0],
        "EMA_200": [5.0, 20.0, 60.0],
        "EOM_14_100000000": [-0.5, 0.0, 0.5],
        "MACD_12_26_9": [10.0, 20.0, 30.0],
        "MACDs_12_26_9": [20.0, 20.0, 20.0],
        "MFI_14": [30.0, 50.0, 70.0],
        "ROC_14": [-0.2, 0.0, 0.2],
        "RSI_14": [30.0, 50.0, 70.0],
        "SMA_15": [5.0, 20.0, 60.0],
        "SMA_40": [5.0, 20.0, 60.0],
        "TRIX_14_9": [1.0, 2.0, 3.0],
        "TRIXs_14_9": [2.0, 2.0, 2.0],
        "WILLR_10": [-30.0, -50.0, -70.0],
    }
    company.technicals = pd.DataFrame(technical_data, index=technical_index)
    return company
