import random

from app.genetic.genes.gene import Gene


class PENowGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['>', '<'])
        self.compared_value = random.uniform(2, 40)

    def condition(self, company, day):
        quarter = Gene.date_to_quarter(day)
        if company.fundamentals.at[quarter, 'EPS'] is None or company.fundamentals.at[quarter, 'EPS'] == 0:
            return False
        indicator_value = company.technicals.at[day, 'Close'] / \
                          company.fundamentals.at[quarter, 'EPS']

        if self.comparator == '>':
            return indicator_value > self.compared_value
        else:
            return indicator_value < self.compared_value

    def condition_to_string(self):
        return "P/E Now %s %s" % (self.comparator, "{0:.2f}".format(self.compared_value))
