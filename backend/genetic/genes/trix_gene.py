from backend.genetic.gene import Gene
import random


class TrixGene(Gene):

    def __init__(self):
        self.comparator = random.choice(['more_than', 'less_than'])
        self.result_true = random.uniform(-10, 10)
        self.result_false = random.uniform(-10, 10)

    def get_substrength(self, company, day):
        indicator_value = company.technicals.at[day, 'trix']
        signal_value = company.technicals.at[day, 'trix_signal']

        if self.comparator == 'more_than':
            if indicator_value > signal_value:
                return self.result_true
            else:
                return self.result_false
        else:
            if indicator_value < signal_value:
                return self.result_true
            else:
                return self.result_false
