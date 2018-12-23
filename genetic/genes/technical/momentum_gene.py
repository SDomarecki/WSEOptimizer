from genetic.genes.gene import Gene
import random


class MomentumGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['>', '<'])
        self.compared_value = random.uniform(-0.25, 0.25)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, 'momentum']

        if self.comparator == '>':
            return indicator_value > self.compared_value
        else:
            return indicator_value < self.compared_value

    def condition_to_string(self):
        return "Momentum %s %s" % (self.comparator, "{0:.2f}".format(self.compared_value))
