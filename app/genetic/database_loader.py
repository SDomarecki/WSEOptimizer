import pandas as pd

from app.genetic.config import Config
from app.shared.company import Company


class DatabaseLoader:

    def __init__(self, path_to_database: str, benchmark_ticker: str):
        self.path = path_to_database
        self.learning_database = None
        self.learning_database_chunks = []
        self.testing_databases = []
        self.benchmark = None
        self.benchmark_learning_wallet = None
        self.benchmark_testing_wallets = []
        self.targets = []

        self.__read_database()
        self.__split_database_equally(Config.chunks)
        self.__read_benchmark(benchmark_ticker)
        self.__calculate_targets()
        self.__calculate_wallets()

    def __read_database(self):
        import json
        import os

        files = os.listdir(self.path + '/basic_info')

        database = {}
        for file in files:
            with open(self.path + '/basic_info/' + file) as data_file:
                json_str = json.loads(data_file.read())
                company = self.__decode_company(json_str)
                if Config.sectors and company.sector not in Config.sectors:
                    print(company.sector + " wtf")
                    continue

            ticker = file.split('.')[0]
            company.fundamentals = self.__get_fundamentals(ticker)
            company.technicals = self.__get_technicals(ticker)
            database[ticker] = company

        sectors = []
        for company in database.values():
            if company.sector not in sectors:
                sectors.append(company.sector)
        print(sectors)

        self.learning_database = self.__filter_database_by_dates(database, Config.start_date, Config.end_date)
        self.testing_databases = [self.__filter_database_by_dates(database, val[0], val[1]) for val in
                                  Config.validations]

    def __decode_company(self, json) -> Company:
        company = Company(json['name'], json['ticker'], json['link'])
        company.sector = json['sector']
        return company

    def __get_fundamentals(self, ticker: str):
        df = pd.read_csv(self.path + '/fundamental/' + ticker + '.csv', delimiter=',', index_col=0)
        return df

    def __get_technicals(self, ticker: str):
        df = pd.read_csv(self.path + '/technical/' + ticker + '.csv', delimiter=',', index_col='Date')
        df.index = pd.to_datetime(df.index)
        return df

    def __filter_database_by_dates(self, database, start_date, end_date):
        from copy import deepcopy

        to_delete = []
        new_database = deepcopy(database)
        for company in new_database.values():
            company.technicals = company.technicals.loc[start_date:end_date]

            circulation_mean = float(company.technicals['Circulation'].mean())
            if Config.min_circulation != -1 and circulation_mean < Config.min_circulation:
                to_delete.append(company.ticker)
            if Config.max_circulation != -1 and circulation_mean > Config.max_circulation:
                to_delete.append(company.ticker)

        for ticker in to_delete:
            del new_database[ticker]

        return new_database

    def __split_database_equally(self, chunks):
        self.learning_database_chunks = [dict() for _ in range(chunks)]
        idx = 0
        for k, v in self.learning_database.items():
            self.learning_database_chunks[idx][k] = v
            if idx < chunks - 1:  # indexes start at 0
                idx += 1
            else:
                idx = 0

    def __read_benchmark(self, ticker: str):
        ticker = ticker.lower()
        df = pd.read_csv(self.path + '/benchmarks/' + ticker + '.csv',
                         delimiter=';',
                         index_col=0)
        df.index = pd.to_datetime(df.index)
        self.benchmark = df

    def __calculate_targets(self):
        target = round(Config.start_cash * self.__get_target_ratio(Config.start_date, Config.end_date), 2)
        self.targets.append(target)
        print('Learning target: %s' % target)

        for idx, el in enumerate(Config.validations):
            target = round(Config.start_cash * self.__get_target_ratio(el[0], el[1]), 2)
            self.targets.append(target)
            print('Validation %s target: %s' % (idx, target))

    def __get_target_ratio(self, start_date, end_date) -> float:
        start_value = DatabaseLoader.__get_closest_value(self.benchmark, start_date)
        end_value = DatabaseLoader.__get_closest_value(self.benchmark, end_date)
        return end_value / start_value

    def __calculate_wallets(self):
        self.benchmark_learning_wallet = self.__calculate_benchmark_wallet(Config.start_date, Config.end_date)
        for idx, el in enumerate(Config.validations):
            self.benchmark_testing_wallets.append(self.__calculate_benchmark_wallet(el[0], el[1]))

    def __calculate_benchmark_wallet(self, start_date, end_date):
        start_cash = Config.start_cash
        import datetime
        delta = datetime.timedelta(days=Config.timedelta)
        start_value = DatabaseLoader.__get_closest_value(self.benchmark, start_date)
        history = []
        day = start_date
        while day < end_date:
            today_value = DatabaseLoader.__get_closest_value(self.benchmark, day)
            history.append(start_cash * today_value / start_value)
            day += delta
        return history

    @staticmethod
    def __get_closest_value(df, date) -> float:
        import datetime
        delta = datetime.timedelta(days=1)

        while True:
            try:
                return df.at[date, 'Zamkniecie']
            except KeyError:
                date -= delta
                continue
