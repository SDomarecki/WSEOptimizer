import json
import os
from copy import deepcopy

import pandas as pd

from app.config import Config
from app.economics.company import Company
from app.genetic.learning_database import LearningDatabase
from app.genetic.testing_database import TestingDatabase


class DatabaseLoader:
    def __init__(self, path_to_database: str, config: Config):
        self.config = config
        self.path = path_to_database

        self.benchmark = None

        self.learning_database: LearningDatabase
        self.testing_databases: [TestingDatabase] = []

        self.__read_database()
        self.__read_benchmark(config.benchmark)

    def __read_database(self):
        tickers = self.__get_tickers_to_read()
        database = []
        for ticker in tickers:
            company = self.__read_one_company(ticker)
            database += [company] if company is not None else []

        self.learning_database = LearningDatabase()
        self.learning_database.companies = self.__filter_database(
            database, self.config.start_date, self.config.end_date
        )
        for (start_date, end_date) in self.config.validations:
            companies = self.__filter_database(database, start_date, end_date)
            testing_database = TestingDatabase()
            testing_database.companies = companies
            self.testing_databases.append(testing_database)

    def __get_tickers_to_read(self) -> [str]:
        directories = os.listdir(f"{self.path}")
        tickers = [ticker for ticker in directories if ticker != "benchmarks"]
        return tickers

    def __read_one_company(self, ticker: str):
        with open(f"{self.path}/{ticker}/basic_info.json") as data_file:
            json_dict = json.loads(data_file.read())
        company = self.__decode_company(json_dict)
        if self.config.sectors and company.sector not in self.config.sectors:
            return

        company.fundamentals = self.__get_fundamentals(ticker)
        company.technicals = self.__get_technicals(ticker)
        return company

    @staticmethod
    def __decode_company(json_company: dict) -> Company:
        return Company(
            json_company["name"],
            json_company["ticker"],
            json_company["link"],
            json_company["sector"],
        )

    def __get_fundamentals(self, ticker: str) -> pd.DataFrame:
        return pd.read_csv(
            f"{self.path}/{ticker}/fundamental.csv", delimiter=",", index_col=0
        )

    def __get_technicals(self, ticker: str) -> pd.DataFrame:
        return pd.read_csv(
            f"{self.path}/{ticker}/technical.csv",
            delimiter=",",
            index_col="Date",
            parse_dates=True,
            infer_datetime_format=True,
        )

    def __filter_database(self, database: [], start_date, end_date) -> []:
        new_database = deepcopy(database)
        # self.__filter_database_by_dates(new_database, start_date, end_date)
        new_database = self.__filter_database_by_circulation(new_database)
        return new_database

    @staticmethod
    def __filter_database_by_dates(database: [], start_date, end_date):
        for company in database:
            company.technicals = company.technicals.loc[start_date:end_date]

    def __filter_database_by_circulation(self, database: []) -> []:
        to_delete = []
        for company in database:
            circulation_mean = float(company.technicals["Circulation"].mean())
            if (
                self.config.min_circulation != -1
                and circulation_mean < self.config.min_circulation
            ):
                to_delete.append(company)
            if (
                self.config.max_circulation != -1
                and circulation_mean > self.config.max_circulation
            ):
                to_delete.append(company)

        for company in to_delete:
            database.remove(company)

        return database

    def __read_benchmark(self, ticker: str):
        ticker = ticker.lower()
        df = pd.read_csv(
            f"{self.path}/benchmarks/{ticker}.csv",
            delimiter=",",
            index_col="Date",
            parse_dates=True,
            infer_datetime_format=True,
        )
        self.learning_database.benchmark = df
        for idx, (start_date, end_date) in enumerate(self.config.validations):
            self.testing_databases[idx].benchmark = df
