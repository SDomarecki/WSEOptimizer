import random

from ..gene import Gene


class PBVyy(Gene):
    def __init__(self):
        super().__init__()
        self.comparator = random.choice([">", "<"])
        self.compared_value = random.uniform(0.8, 1.8)

    def condition(self, company, day) -> bool:
        quarter = self.date_to_quarter(day)
        prev_year = self.date_to_previous_year_quarter(day)

        indicator_value = company.fundamentals.at[quarter, "P/BV"]
        previous_indicator_value = company.fundamentals.at[prev_year, "P/BV"]

        if self.comparator == ">":
            return indicator_value / previous_indicator_value > self.compared_value
        return indicator_value / previous_indicator_value < self.compared_value

    def condition_to_string(self) -> str:
        return f"P/BV / PrevY P/BV {self.comparator} {self.compared_value:.2f}"
