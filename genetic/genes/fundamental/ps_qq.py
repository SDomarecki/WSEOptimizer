import random

from genetic.genes.gene import Gene


class PSqq(Gene):

    def __init__(self):
        super().__init__()
        self.comparator = random.choice(['more_than', 'less_than'])

    def condition(self, company, day):
        quarter = Gene.date_to_quarter(day)
        prev_quarter = Gene.date_to_previous_quarter(day)

        indicator_value = company.fundamentals.at[quarter, 'P/S']
        previous_indicator_value = company.fundamentals.at[prev_quarter, 'P/S']

        compared_value = random.uniform(-0.5, 0.5)

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
        return "P/S " + c + " PrevQ P/S"
