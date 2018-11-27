import random
import pandas as pd

from config import Config


class Gene:

    def __init__(self):

        self.result_true = random.randint(1, 10) * random.choice([-1, 1])
        self.result_false = random.randint(1, 10) * random.choice([-1, 1])

    def get_substrength(self, company, day) -> int:
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
        import datetime
        fin_statement_lag = datetime.timedelta(days=Config.fin_statement_lag)
        lag_date = date - fin_statement_lag
        return str(lag_date.year) + "/Q" + str(pd.Timestamp(lag_date).quarter)
