from abc import ABC
from datetime import date

from app.economics.company import Company
from app.genetic.genes.fundamental.gene_fundamental import GeneFundamental


class GeneCurrentValue(GeneFundamental, ABC):
    def __init__(self):
        super().__init__()
        self.indicator = ""
        self.denominator_indicator = ""
        self.compared_value = 0.0

    def condition(self, company: Company, day: date) -> bool:
        quarter = self.date_to_quarter(day)
        quarter_value = company.fundamentals.at[quarter, "EPS"]
        if quarter_value is None or quarter_value == 0:
            return False
        indicator_value = company.technicals.at[day, "close"] / quarter_value

        if self.comparator == ">":
            return indicator_value > self.compared_value
        return indicator_value < self.compared_value

    def condition_to_string(self) -> str:
        return f"{self.indicator} Now {self.comparator} {self.compared_value:.2f}"
