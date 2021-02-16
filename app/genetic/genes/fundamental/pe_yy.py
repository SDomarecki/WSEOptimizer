import random

from app.genetic.genes.gene import Gene


class PEyy(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['>', '<'])
        self.compared_value = random.uniform(0.8, 1.8)

    def condition(self, company, day):
        quarter = Gene.date_to_quarter(day)
        prev_year = Gene.date_to_previous_year_quarter(day)

        indicator_value = company.fundamentals.at[quarter, 'P/E']
        previous_indicator_value = company.fundamentals.at[prev_year, 'P/E']

        if self.comparator == '>':
            return indicator_value / previous_indicator_value > self.compared_value
        else:
            return indicator_value / previous_indicator_value < self.compared_value

    def condition_to_string(self):
        return "P/E / PrevY P/E %s %s" % (self.comparator, self.compared_value)