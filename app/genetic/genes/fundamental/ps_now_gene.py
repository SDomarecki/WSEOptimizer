import random

from ..gene import Gene


class PSNowGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['>', '<'])
        self.compared_value = random.uniform(2, 40)

    def condition(self, company, day) -> bool:
        quarter = self.date_to_quarter(day)
        indicator_value = company.technicals.at[day, 'Close'] / \
                          company.fundamentals.at[quarter, 'SPS']

        if self.comparator == '>':
            return indicator_value > self.compared_value
        else:
            return indicator_value < self.compared_value

    def condition_to_string(self) -> str:
        return f'P/S Now {self.comparator} {self.compared_value:.2f}'
