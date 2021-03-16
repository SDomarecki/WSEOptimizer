import random
from abc import ABC, abstractmethod
from datetime import date, timedelta

from app.economics.company import Company
from app.genetic.genes.gene import Gene
import pandas as pd


class GeneFundamental(Gene, ABC):
    def __init__(self):
        super().__init__()
        self.statement_lag = 135
        self.comparator = random.choice([">", "<"])

    def date_to_quarter(self, day: date) -> str:
        fin_statement_lag = timedelta(days=self.statement_lag)
        lag_date = day - fin_statement_lag
        return f"{lag_date.year}/Q{pd.Timestamp(lag_date).quarter}"

    @abstractmethod
    def condition(self, company: Company, day: date) -> bool:
        raise NotImplementedError

    @abstractmethod
    def condition_to_string(self) -> str:
        raise NotImplementedError
