from genetic.genes.gene import Gene
import random


class EMVGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['>', '<'])
        self.close_value = random.uniform(-1, 1)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, 'emv']

        if self.comparator == '>':
            return indicator_value > self.close_value
        else:
            return indicator_value < self.close_value

    def condition_to_string(self):
        return "EMV %s Close" % self.comparator
