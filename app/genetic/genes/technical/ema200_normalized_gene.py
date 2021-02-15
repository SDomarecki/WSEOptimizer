import random

from app.genetic.genes.gene import Gene


class EMA200NormalizedGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['>', '<'])
        self.compared_value = random.uniform(0.5, 2)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, 'ema200']
        close_value = company.technicals.at[day, 'Close']
        normalized_value = indicator_value / close_value

        if self.comparator == '>':
            return normalized_value > self.compared_value
        else:
            return normalized_value < self.compared_value

    def condition_to_string(self):
        return "EMA200Norm %s %s" % (self.comparator, " {0:.2f}".format(self.compared_value))
