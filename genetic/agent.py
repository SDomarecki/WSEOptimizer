import datetime
import random

from genetic.genes.gene_factory import GeneFactory
from genetic.wallet import Wallet
from shared.config import Config


class Agent:

    def __init__(self, id, length):
        self.id = id
        self.genes = [GeneFactory.create_random_gene() for _ in range(length)]
        self.weights = [random.uniform(0.0,  1.0) for _ in range(length)]
        self.fitness = 0
        self.validation = 0
        self.wallet = Wallet()

    def calculate_fitness(self, database, validation=False):
        self.wallet = Wallet()

        if not validation:
            self.fitness = 0
            start_date = Config.start_date
            end_date = Config.end_date
        else:
            self.validation = 0
            start_date = Config.validation_start_date
            end_date = Config.validation_end_date

        simulation_result = self.simulate(database, start_date, end_date)

        if not validation:
            self.fitness = simulation_result
            print('Agent no. ' + str(self.id) + " fitness - " + str(simulation_result))
        else:
            self.validation = simulation_result
            print('Agent no. ' + str(self.id) + " validation - " + str(simulation_result))

    def simulate(self, database, start_date, end_date) -> float:
        day = start_date
        delta = datetime.timedelta(days=Config.timedelta)
        while day < end_date:
            if day.weekday() == 5:
                day += datetime.timedelta(days=2)
            if day.weekday() == 6:
                day += datetime.timedelta(days=1)

            stock_strengths = {}
            for stock in database.values():
                strength = self.calculate_strength(stock, day)
                stock_strengths[stock] = strength

            ordered_stocks = []
            ordered_tuples = sorted(stock_strengths.items(), key=lambda kv: kv[1], reverse=True)
            for key, value in ordered_tuples:
                ordered_stocks.append(key)

            self.wallet.trade(ordered_stocks, day, database)
            day += delta

        if Config.return_method == "total_value":
            return self.wallet.get_total_value(database, end_date)
        elif Config.return_method == "sharpe":
            return self.wallet.get_current_sharpe(database)
        else:
            return self.wallet.get_current_information_ratio()

    def calculate_strength(self, stock, day) -> float:
        strength = 0
        for i in range(len(self.genes)):
            try:
                strength += self.genes[i].get_substrength(stock, day) * self.weights[i]
            except KeyError:
                continue
        return strength

    def to_json_ready(self):
        return {
            "id": self.id,
            "strategy": self.to_string(),
            "fitness": self.fitness,
            "validation": self.validation
        }

    def to_string(self) -> [str]:
        return list(map(lambda g: g.to_string(), self.genes))
