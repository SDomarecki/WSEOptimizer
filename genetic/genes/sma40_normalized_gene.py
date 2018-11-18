from genetic.gene import Gene
import random


class SMA40NormalizedGene(Gene):

    def __init__(self):
        self.comparator = random.choice(['more_than', 'less_than'])
        self.result_true = random.uniform(-10, 10)
        self.result_false = random.uniform(-10, 10)
        self.compared_value = random.uniform(0.5, 2)

    def get_substrength(self, company, day):
        indicator_value = company.technicals.at[day, 'sma40']
        close_value = company.technicals.at[day, 'Close']
        normalized_value = indicator_value / close_value

        if self.comparator == 'more_than':
            if normalized_value > self.compared_value:
                return self.result_true
            else:
                return self.result_false
        else:
            if normalized_value < self.compared_value:
                return self.result_true
            else:
                return self.result_false
