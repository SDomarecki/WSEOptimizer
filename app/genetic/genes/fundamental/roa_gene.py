import random

from ..gene import Gene


class ROAGene(Gene):
    def __init__(self):
        super().__init__()
        self.comparator = random.choice([">", "<"])
        self.compared_value = random.uniform(-0.5, 0.5)

    def condition(self, company, day) -> bool:
        quarter = self.date_to_quarter(day)
        indicator_value = company.fundamentals.at[quarter, "ROA"]

        if self.comparator == ">":
            return indicator_value > self.compared_value
        return indicator_value < self.compared_value

    def condition_to_string(self) -> str:
        return f"ROA {self.comparator} {self.compared_value:.2f}"
