from genetic.genes.gene import Gene
import random


class MACDGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['>', '<'])

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, 'macd_val']
        signal_value = company.technicals.at[day, 'macd_signal_line']

        if self.comparator == '>':
            return indicator_value > signal_value
        else:
            return indicator_value < signal_value

    def condition_to_string(self):
        return "MACD %s MACD Signal" % self.comparator
