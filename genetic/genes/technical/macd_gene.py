from genetic.genes.gene import Gene
import random


class MACDGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['more_than', 'less_than'])

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, 'macd_val']
        signal_value = company.technicals.at[day, 'macd_signal_line']

        if self.comparator == 'more_than':
            if indicator_value > signal_value:
                return True
            else:
                return False
        else:
            if indicator_value < signal_value:
                return True
            else:
                return False

    def condition_to_string(self):
        if self.comparator == 'more_than':
            c = ">"
        else:
            c = "<"
        return "MACD " + c + " MACD Signal"
