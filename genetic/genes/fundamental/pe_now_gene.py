import random

from genetic.genes.gene import Gene


class PENowGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['more_than', 'less_than'])
        self.compared_value = random.uniform(2, 40)

    def condition(self, company, day):
        quarter = Gene.date_to_quarter(day)
        if company.fundamentals.at[quarter, 'EPS'] is None or company.fundamentals.at[quarter, 'EPS'] == 0:
            return False
        indicator_value = company.technicals.at[day, 'Close'] / \
                          company.fundamentals.at[quarter, 'EPS']

        if self.comparator == 'more_than':
            if indicator_value > self.compared_value:
                return True
            else:
                return False
        else:
            if indicator_value < self.compared_value:
                return True
            else:
                return False

    def condition_to_string(self):
        if self.comparator == 'more_than':
            c = ">"
        else:
            c = "<"
        return "P/E Now " + c + " {0:.2f}".format(self.compared_value)
