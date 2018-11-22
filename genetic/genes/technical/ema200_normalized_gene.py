from genetic.genes.gene import Gene
import random


class EMA200NormalizedGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['more_than', 'less_than'])
        self.compared_value = random.uniform(0.5, 2)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, 'ema200']
        close_value = company.technicals.at[day, 'Close']
        normalized_value = indicator_value / close_value

        if self.comparator == 'more_than':
            if normalized_value > self.compared_value:
                return True
            else:
                return False
        else:
            if normalized_value < self.compared_value:
                return True
            else:
                return False

    def to_string(self):
        if self.comparator == 'more_than':
            c = ">"
        else:
            c = "<"
        return "If(EMA200Norm " \
               + c \
               + " " \
               + "{0:.2f}".format(self.compared_value) \
               + ") then " \
               + str(self.result_true) \
               + " else " \
               + str(self.result_false)
