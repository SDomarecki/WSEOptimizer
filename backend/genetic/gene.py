# if(indicator comparator value):
#     return result_true
# else:
#     return result_false
#
# W uogólnieniu value i indicator mogłyby być zamienne oraz result_true/false byłyby kolejnymi genami

class Gene:
    indicator = None  #string?
    comparator = None #string - less than, more than, equals?
    value = 0
    result_true = 0
    result_false = 0

    def __init__(self, indicator, comparator, value, result_true, result_false):
        self.indicator = indicator
        self.comparator = comparator
        self.value = value
        self.result_true = result_true
        self.result_false = result_false

    def get_substrength(self, company, day):
        if self.indicator.type == 'fundamental':
            indicator_value = self.get_fundamental_strength(company.fundamentals, day)
        else:
            indicator_value = self.get_technical_strength(company.technicals, day)

        if self.comparator == 'more_than':
            if indicator_value > self.value:
                return self.result_true
            else:
                return self.result_false
        elif self.comparator == 'less_than':
            if indicator_value < self.value:
                return self.result_true
            else:
                return self.result_false
        else:
            if indicator_value == self.value:
                return self.result_true
            else:
                return self.result_false

    def get_fundamental_strength(self, fundamentals, day):
        from shared.model.company import date_to_quarter
        quarter = date_to_quarter(day)
        financial_statement = fundamentals[quarter]
        return financial_statement[self.indicator]

    def get_technical_strength(self, technicals, day):
        stock_day = technicals[day]
        return stock_day[self.indicator]


def create_random_gene():
    possible_indicators = ['SMA_15_NORM', 'SMA_40_NORM', 'SMA_200_NORM', 'RSI', 'MFI']

    import random
    indicator = random.choice(possible_indicators)
    #TODO More randomic!!
    comparator = 'more_than'
    value = 0.5
    result_true = 50
    result_false = -50

    return Gene(indicator, comparator, value, result_true, result_false)