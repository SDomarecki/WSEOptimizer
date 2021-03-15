from abc import ABC
from datetime import date, timedelta

import pandas as pd

from app.economics.company import Company
from app.genetic.genes.fundamental.gene_fundamental import GeneFundamental


class GeneYYChange(GeneFundamental, ABC):
    def __init__(self):
        super().__init__()
        self.indicator = ""
        self.compared_value = 0.0

    def condition(self, company: Company, day: date) -> bool:
        quarter = self.date_to_quarter(day)
        prev_year = self.date_to_previous_year_quarter(day)

        indicator_value = company.fundamentals.at[quarter, self.indicator]
        previous_indicator_value = company.fundamentals.at[prev_year, self.indicator]

        if previous_indicator_value == 0:
            previous_indicator_value = 0.1

        if self.comparator == ">":
            return indicator_value / previous_indicator_value > self.compared_value
        return indicator_value / previous_indicator_value < self.compared_value

    def date_to_previous_year_quarter(self, day: date) -> str:
        fin_statement_lag = timedelta(days=self.statement_lag + 365)
        lag_date = day - fin_statement_lag
        return f"{lag_date.year}/Q{pd.Timestamp(lag_date).quarter}"

    def condition_to_string(self) -> str:
        return f"{self.indicator} / PrevY {self.indicator} {self.comparator} {self.compared_value:.2f}"
