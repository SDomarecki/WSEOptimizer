import datetime
import json
import os
from copy import deepcopy

import pandas as pd

from app.config import Config
from app.economics.company import Company
from app.genetic.get_closest_value import get_closest_value


class DatabaseLoader:
    def __init__(self, path_to_database: str, config: Config):
        self.config = config
        self.path = path_to_database

        self.learning_database = None
        self.learning_database_chunks = []
        self.testing_databases = []
        self.benchmark = None
        self.benchmark_learning_wallet = None
        self.benchmark_testing_wallets = []
        self.targets = []

        self.__read_database()
        self.__split_database_equally()

        self.__read_benchmark(config.benchmark)
        self.__calculate_targets()
        self.__calculate_wallets()

    def __read_database(self):
        directories = os.listdir(f"{self.path}")
        tickers = [ticker for ticker in directories if ticker != "benchmarks"]

        database = {}
        for ticker in tickers:
            with open(f"{self.path}/{ticker}/basic_info.json") as data_file:
                json_dict = json.loads(data_file.read())
            company = self.__decode_company(json_dict)
            if self.config.sectors and company.sector not in self.config.sectors:
                continue

            company.fundamentals = self.__get_fundamentals(ticker)
            company.technicals = self.__get_technicals(ticker)
            database[ticker] = company

        self.learning_database = self.__filter_database(
            database, self.config.start_date, self.config.end_date
        )
        self.testing_databases = [
            self.__filter_database(database, val[0], val[1])
            for val in self.config.validations
        ]

    @staticmethod
    def __decode_company(json_company: dict) -> Company:
        return Company(
            json_company["name"],
            json_company["ticker"],
            json_company["link"],
            json_company["sector"],
        )

    def __get_fundamentals(self, ticker: str) -> pd.DataFrame:
        df = pd.read_csv(
            f"{self.path}/{ticker}/fundamental.csv", delimiter=",", index_col=0
        )
        return df

    def __get_technicals(self, ticker: str) -> pd.DataFrame:
        df = pd.read_csv(
            f"{self.path}/{ticker}/technical.csv",
            delimiter=",",
            index_col="Date",
            parse_dates=True,
            infer_datetime_format=True,
        )
        return df

    def __filter_database(self, database, start_date, end_date) -> dict:
        new_database = deepcopy(database)
        self.__filter_database_by_dates(new_database, start_date, end_date)
        self.__filter_database_by_circulation(new_database)
        return new_database

    @staticmethod
    def __filter_database_by_dates(database: dict, start_date, end_date):
        for company in database.values():
            company.technicals = company.technicals.loc[start_date:end_date]

    def __filter_database_by_circulation(self, database: dict) -> dict:
        to_delete = []
        for company in database.values():
            circulation_mean = float(company.technicals["Circulation"].mean())
            if (
                self.config.min_circulation != -1
                and circulation_mean < self.config.min_circulation
            ):
                to_delete.append(company.ticker)
            if (
                self.config.max_circulation != -1
                and circulation_mean > self.config.max_circulation
            ):
                to_delete.append(company.ticker)

        for ticker in to_delete:
            del database[ticker]

        return database

    def __split_database_equally(self):
        chunks = self.config.chunks
        self.learning_database_chunks = [{} for _ in range(chunks)]
        idx = 0
        for k, v in self.learning_database.items():
            self.learning_database_chunks[idx][k] = v
            if idx < chunks - 1:
                idx += 1
            else:
                idx = 0

    def __read_benchmark(self, ticker: str):
        ticker = ticker.lower()
        df = pd.read_csv(
            f"{self.path}/benchmarks/{ticker}.csv",
            delimiter=",",
            index_col="Date",
            parse_dates=True,
            infer_datetime_format=True,
        )
        self.benchmark = df

    def __calculate_targets(self):
        target = round(
            self.config.start_cash
            * self.__get_target_ratio(self.config.start_date, self.config.end_date),
            2,
        )
        self.targets.append(target)
        print(f"Learning target: {target}")

        for idx, el in enumerate(self.config.validations):
            target = round(
                self.config.start_cash * self.__get_target_ratio(el[0], el[1]), 2
            )
            self.targets.append(target)
            print(f"Validation {idx} target: {target}")

    def __get_target_ratio(self, start_date, end_date) -> float:
        start_value = get_closest_value(self.benchmark, start_date, "Close")
        end_value = get_closest_value(self.benchmark, end_date, "Close")
        return end_value / start_value

    def __calculate_wallets(self):
        self.benchmark_learning_wallet = self.__calculate_benchmark_wallet(
            self.config.start_date, self.config.end_date
        )
        for validation in self.config.validations:
            self.benchmark_testing_wallets.append(
                self.__calculate_benchmark_wallet(validation[0], validation[1])
            )

    def __calculate_benchmark_wallet(self, start_date, end_date):
        start_cash = self.config.start_cash
        delta = datetime.timedelta(days=self.config.timedelta)
        start_value = get_closest_value(self.benchmark, start_date, "Close")
        history = []
        day = start_date
        while day < end_date:
            today_value = get_closest_value(self.benchmark, day, "Close")
            history.append(start_cash * today_value / start_value)
            day += delta
        return history
