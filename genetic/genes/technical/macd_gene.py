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

    def to_string(self):
        if self.comparator == 'more_than':
            c = ">"
        else:
            c = "<"
        return "If(MACD " \
               + c \
               + " MACD Signal) then " \
               + str(self.result_true) \
               + " else " \
               + str(self.result_false)