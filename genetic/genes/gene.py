# if(indicator comparator value):
#     return result_true
# else:
#     return result_false
#
# W uogólnieniu value i indicator mogłyby być zamienne oraz result_true/false byłyby kolejnymi genami
import random
import pandas as pd


class Gene:

    def __init__(self):
        self.result_true = random.uniform(-10, 10)
        self.result_false = random.uniform(-10, 10)

    def get_substrength(self, company, day) -> float:
        if self.condition(company, day):
            return self.result_true
        else:
            return self.result_false

    def condition(self, company, day) -> bool:
        raise NotImplementedError("Please Implement this method")

    def to_string(self) -> str:
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def date_to_quarter(date) -> str:
        return str(date.year) + "/Q" + str(pd.Timestamp(date).quarter)
