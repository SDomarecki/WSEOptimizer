import random

from genetic.genes.gene import Gene


class ROAyy(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['>', '<'])
        self.compared_value = random.uniform(-0.8, 3.0)

    def condition(self, company, day):
        quarter = Gene.date_to_quarter(day)
        prev_year = Gene.date_to_previous_year_quarter(day)

        indicator_value = company.fundamentals.at[quarter, 'ROA']
        previous_indicator_value = company.fundamentals.at[prev_year, 'ROA']

        if previous_indicator_value == 0:
            previous_indicator_value = .1

        if self.comparator == '>':
            return indicator_value/previous_indicator_value -1 > self.compared_value
        else:
            return indicator_value/previous_indicator_value -1 < self.compared_value

    def condition_to_string(self):
        return "ROA / PrevY ROA %s %s" % (self.comparator, self.compared_value)
