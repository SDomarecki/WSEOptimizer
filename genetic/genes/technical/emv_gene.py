from genetic.genes.gene import Gene
import random


class EMVGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['more_than', 'less_than'])
        self.close_value = random.uniform(-1, 1)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, 'emv']

        if self.comparator == 'more_than':
            if indicator_value > self.close_value:
                return True
            else:
                return False
        else:
            if indicator_value < self.close_value:
                return True
            else:
                return False

    def to_string(self):
        if self.comparator == 'more_than':
            c = ">"
        else:
            c = "<"
        return "If(EMV " \
               + c \
               + " Close) then " \
               + str(self.result_true) \
               + " else " \
               + str(self.result_false)