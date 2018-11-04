from backend.genetic.gene import Gene
import random

from shared.model.company import date_to_quarter


class ROAGene(Gene):

    def __init__(self):
        self.comparator = random.choice(['more_than', 'less_than'])
        self.result_true = random.uniform(-10, 10)
        self.result_false = random.uniform(-10, 10)
        self.compared_value = random.uniform(-0.5, 0.5)

    def get_substrength(self, company, day):
        quarter = date_to_quarter(day)
        indicator_value = company.fundamentals.at[quarter, 'ROA']

        if self.comparator == 'more_than':
            if indicator_value > self.compared_value:
                return self.result_true
            else:
                return self.result_false
        else:
            if indicator_value < self.compared_value:
                return self.result_true
            else:
                return self.result_false
