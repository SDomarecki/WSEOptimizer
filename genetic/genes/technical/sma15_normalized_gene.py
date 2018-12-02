from genetic.genes.gene import Gene
import random


class SMA15NormalizedGene(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['more_than', 'less_than'])
        self.compared_value = random.uniform(0.5, 2)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, 'sma15']
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

    def condition_to_string(self):
        if self.comparator == 'more_than':
            c = ">"
        else:
            c = "<"
        return "SMA15Norm " + c + " {0:.2f}".format(self.compared_value)
