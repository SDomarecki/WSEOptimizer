import random

from genetic.genes.gene import Gene


class PEGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['more_than', 'less_than'])
        self.compared_value = random.uniform(2, 40)

    def condition(self, company, day):
        quarter = Gene.date_to_quarter(day)
        indicator_value = company.fundamentals.at[quarter, 'P/E']
        if indicator_value is None:
            return False

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
        return "P/E " + c + " {0:.2f}".format(self.compared_value)
