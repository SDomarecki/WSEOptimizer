import datetime

from app.config import Config
from app.genetic.get_closest_value import get_closest_value
from app.genetic.learning_database import LearningDatabase
from app.genetic.testing_database import TestingDatabase


class BenchmarkAgent:
    def __init__(self, config: Config):
        self.config = config

    def calculate_benchmarks(self, learning_database, testing_databases):
        self.__calculate_learning_target(learning_database)
        self.__calculate_testing_targets(testing_databases)
        self.__calculate_learning_benchmark_wallet(learning_database)
        self.__calculate_testing_benchmark_wallets(testing_databases)

    def __calculate_learning_target(self, learning_database: LearningDatabase):
        target = self.config.start_cash * self.__get_target_ratio(
            learning_database.benchmark, self.config.start_date, self.config.end_date
        )
        target = round(target, 2)
        learning_database.benchmark_target = target
        print(f"Learning target: {target}")

    def __calculate_testing_targets(self, testing_databases: [TestingDatabase]):
        for idx, (start_date, end_date) in enumerate(self.config.validations):
            target = self.config.start_cash * self.__get_target_ratio(
                testing_databases[idx].benchmark, start_date, end_date
            )
            target = round(target, 2)
            testing_databases[idx].benchmark_target = target
            print(f"Testing {idx} target: {target}")

    @staticmethod
    def __get_target_ratio(benchmark, start_date, end_date) -> float:
        start_value = get_closest_value(benchmark, start_date, "Close")
        end_value = get_closest_value(benchmark, end_date, "Close")
        return end_value / start_value

    def __calculate_learning_benchmark_wallet(self, learning_database):
        learning_database.benchmark_wallet = self.__calculate_benchmark_wallet(
            learning_database.benchmark, self.config.start_date, self.config.end_date
        )

    def __calculate_testing_benchmark_wallets(self, testing_databases):
        for idx, (start_date, end_date) in enumerate(self.config.validations):
            testing_databases[idx].benchmark_wallet = self.__calculate_benchmark_wallet(
                testing_databases[idx].benchmark, start_date, end_date
            )

    def __calculate_benchmark_wallet(self, benchmark, start_date, end_date):
        start_cash = self.config.start_cash
        delta = datetime.timedelta(days=self.config.timedelta)
        start_value = get_closest_value(benchmark, start_date, "Close")
        history = []
        day = start_date
        while day < end_date:
            today_value = get_closest_value(benchmark, day, "Close")
            history.append(start_cash * today_value / start_value)
            day += delta
        return history
