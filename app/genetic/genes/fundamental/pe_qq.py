import random

from ..gene import Gene


class PEqq(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['>', '<'])
        self.compared_value = random.uniform(0.5, 1.5)

    def condition(self, company, day) -> bool:
        quarter = self.date_to_quarter(day)
        prev_quarter = self.date_to_previous_quarter(day)

        indicator_value = company.fundamentals.at[quarter, 'P/E']
        previous_indicator_value = company.fundamentals.at[prev_quarter, 'P/E']

        if self.comparator == '>':
            return indicator_value / previous_indicator_value > self.compared_value
        else:
            return indicator_value / previous_indicator_value < self.compared_value

    def condition_to_string(self) -> str:
        return f'P/E / PrevQ P/E {self.comparator} {self.compared_value:.2f}'
