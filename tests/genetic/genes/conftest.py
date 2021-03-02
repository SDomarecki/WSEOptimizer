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
        "BVPS": [10.0, 10.0, 10.0, 10.0, 10.0],
    }
    company.fundamentals = pd.DataFrame(fundamental_data, index=fundamental_index)
    technical_index = [date(2000, 6, 1), date(2001, 1, 1), date(2001, 6, 1)]
    technical_data = {"Close": [10.0, 20.0, 30.0]}
    company.technicals = pd.DataFrame(technical_data, index=technical_index)
    return company
