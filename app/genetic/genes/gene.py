import random
from datetime import date, timedelta

import pandas as pd

from app.economics.company import Company


class Gene:
    def __init__(self):
        self.statement_lag = 135
        self.result_true = random.randint(1, 10) * random.choice([-1, 1])
        self.result_false = random.randint(1, 10) * random.choice([-1, 1])
        while self.result_false == self.result_true:
            self.result_false = random.randint(1, 10) * random.choice([-1, 1])
        self.weight = round(random.uniform(0.0, 1.0), 2)

    def get_substrength(self, company: Company, day: date) -> float:
        try:
            if self.condition(company, day):
                return self.weight * self.result_true
            else:
                return self.weight * self.result_false
        except KeyError:
            return 0.0

    def condition(self, company: Company, day: date) -> bool:
        raise NotImplementedError("Please Implement this method")

    def to_string(self) -> str:
        return f"{self.weight:.2f} x If({self.condition_to_string()}) then {self.result_true} else {self.result_false}"

    def condition_to_string(self) -> str:
        raise NotImplementedError("Please Implement this method")

    def date_to_quarter(self, day: date) -> str:
        fin_statement_lag = timedelta(days=self.statement_lag)
        lag_date = day - fin_statement_lag
        return f"{lag_date.year}/Q{pd.Timestamp(lag_date).quarter}"

    def date_to_previous_quarter(self, day: date) -> str:
        fin_statement_lag = timedelta(days=self.statement_lag + 90)
        lag_date = day - fin_statement_lag
        return f"{lag_date.year}/Q{pd.Timestamp(lag_date).quarter}"

    def date_to_previous_year_quarter(self, day: date) -> str:
        fin_statement_lag = timedelta(days=self.statement_lag + 365)
        lag_date = day - fin_statement_lag
        return f"{lag_date.year}/Q{pd.Timestamp(lag_date).quarter}"
