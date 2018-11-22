from genetic.genes.gene import Gene
import random


class MomentumGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['more_than', 'less_than'])
        self.compared_value = random.uniform(-0.25, 0.25)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, 'momentum']

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
        return "If(Momentum " \
               + c \
               + " " \
               + "{0:.2f}".format(self.compared_value) \
               + ") then " \
               + str(self.result_true) \
               + " else " \
               + str(self.result_false)