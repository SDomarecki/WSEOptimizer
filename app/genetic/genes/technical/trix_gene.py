import random

from ..gene import Gene


class TrixGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['>', '<'])

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, 'trix']
        signal_value = company.technicals.at[day, 'trix_signal']

        if self.comparator == '>':
            return indicator_value > signal_value
        else:
            return indicator_value < signal_value

    def condition_to_string(self) -> str:
        return f'Trix {self.comparator} Trix Signal'
