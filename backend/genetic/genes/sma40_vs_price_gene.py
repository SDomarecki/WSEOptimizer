from backend.genetic.gene import Gene
import random


class SMA40VsPriceGene(Gene):

    def __init__(self):
        self.comparator = random.choice(['more_than', 'less_than'])
        self.result_true = random.uniform(-10, 10)
        self.result_false = random.uniform(-10, 10)

    def get_substrength(self, company, day):
        indicator_value = company.technicals.at[day, 'sma40']
        close_value = company.technicals.at[day, 'Close']

        if self.comparator == 'more_than':
            if indicator_value > close_value:
                return self.result_true
            else:
                return self.result_false
        else:
            if indicator_value < close_value:
                return self.result_true
            else:
                return self.result_false
