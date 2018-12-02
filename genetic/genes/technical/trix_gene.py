from genetic.genes.gene import Gene
import random


class TrixGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['more_than', 'less_than'])

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, 'trix']
        signal_value = company.technicals.at[day, 'trix_signal']

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
        return "Trix " + c + " Trix Signal"
