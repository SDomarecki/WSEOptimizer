import random

from genetic.gene import Gene


class PEGene(Gene):

    def __init__(self):
        self.comparator = random.choice(['more_than', 'less_than'])
        self.result_true = random.uniform(-10, 10)
        self.result_false = random.uniform(-10, 10)
        self.compared_value = random.uniform(2, 40)

    def get_substrength(self, company, day):
        quarter = Gene.date_to_quarter(day)
        indicator_value = company.fundamentals.at[quarter, 'P/E']
        if indicator_value is None:
            return 0

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
