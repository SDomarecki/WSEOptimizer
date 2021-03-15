from abc import ABC
from datetime import date

from app.economics.company import Company
from app.genetic.genes.fundamental.gene_fundamental import GeneFundamental


class GeneStatementValue(GeneFundamental, ABC):
    def __init__(self):
        super().__init__()
        self.indicator = ""
        self.compared_value = 0.0

    def condition(self, company: Company, day: date) -> bool:
        quarter = self.date_to_quarter(day)
        indicator_value = company.fundamentals.at[quarter, self.indicator]

        if indicator_value is None:
            indicator_value = -1

        if self.comparator == ">":
            return indicator_value > self.compared_value
        return indicator_value < self.compared_value

    def condition_to_string(self) -> str:
        return f"{self.indicator} {self.comparator} {self.compared_value:.2f}"
