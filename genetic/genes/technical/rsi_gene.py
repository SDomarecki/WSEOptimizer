from genetic.genes.gene import Gene
import random


class RSIGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['more_than', 'less_than'])
        self.compared_value = random.uniform(20,80)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, 'rsi']

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
        return "RSI " + c + " {0:.2f}".format(self.compared_value)
