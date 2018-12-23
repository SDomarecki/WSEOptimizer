import random
import pandas as pd

from config import Config


class Gene:

    def __init__(self):
        self.result_true = random.randint(1, 10) * random.choice([-1, 1])
        self.result_false = random.randint(1, 10) * random.choice([-1, 1])
        self.weight = round(random.uniform(0.0, 1.0), 2)

    def get_substrength(self, company, day) -> float:
        try:
            if self.condition(company, day):
                return self.weight * self.result_true
            else:
                return self.weight * self.result_false
        except KeyError:
            return 0

    def condition(self, company, day) -> bool:
        raise NotImplementedError("Please Implement this method")

    def to_string(self) -> str:
        return "%s x If(%s) then %s else %s" % \
               ("{0:.2f}".format(self.weight), self.condition_to_string(),
                self.result_true, self.result_false)

    def condition_to_string(self) -> str:
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def date_to_quarter(date) -> str:
        import datetime
        fin_statement_lag = datetime.timedelta(days=Config.fin_statement_lag)
        lag_date = date - fin_statement_lag
        return "%s/Q%s" % (lag_date.year, pd.Timestamp(lag_date).quarter)

    @staticmethod
    def date_to_previous_quarter(date) -> str:
        import datetime
        fin_statement_lag = datetime.timedelta(days=Config.fin_statement_lag+90)
        lag_date = date - fin_statement_lag
        return "%s/Q%s" % (lag_date.year, pd.Timestamp(lag_date).quarter)

    @staticmethod
    def date_to_previous_year_quarter(date) -> str:
        import datetime
        fin_statement_lag = datetime.timedelta(days=Config.fin_statement_lag+365)
        lag_date = date - fin_statement_lag
        return "%s/Q%s" % (lag_date.year, pd.Timestamp(lag_date).quarter)

