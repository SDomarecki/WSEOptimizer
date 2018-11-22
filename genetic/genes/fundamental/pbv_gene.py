import random

from genetic.genes.gene import Gene


class PBVGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['more_than', 'less_than'])
        self.compared_value = random.uniform(0.25, 4)

    def condition(self, company, day):
        quarter = Gene.date_to_quarter(day)
        indicator_value = company.fundamentals.at[quarter, 'P/BV']

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

    def to_string(self):
        if self.comparator == 'more_than':
            c = ">"
        else:
            c = "<"
        return "If(P/BV " \
               + c \
               + " " \
               + "{0:.2f}".format(self.compared_value) \
               + ") then " \
               + str(self.result_true) \
               + " else " \
               + str(self.result_false)
