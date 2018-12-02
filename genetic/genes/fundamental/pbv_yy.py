import random

from genetic.genes.gene import Gene


class PBVyy(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['more_than', 'less_than'])

    def condition(self, company, day):
        quarter = Gene.date_to_quarter(day)
        prev_year = Gene.date_to_previous_year_quarter(day)

        indicator_value = company.fundamentals.at[quarter, 'P/BV']
        previous_indicator_value = company.fundamentals.at[prev_year, 'P/BV']

        compared_value = random.uniform(-0.8, 0.8)

        if self.comparator == 'more_than':
            if indicator_value/previous_indicator_value -1 > compared_value:
                return True
            else:
                return False
        else:
            if indicator_value/previous_indicator_value -1 < compared_value:
                return True
            else:
                return False

    def condition_to_string(self):
        if self.comparator == 'more_than':
            c = ">"
        else:
            c = "<"
        return "P/BV " + c + " PrevY P/BV"
