import datetime

from app.config import Config
from app.economics.trader import Trader
from app.genetic.genes.gene import Gene


class Agent:
    def __init__(self, agent_id, genome: [Gene], config: Config):
        self.agent_id = agent_id
        self.genome = genome
        self.trader = Trader(config)
        self.config = config
        self.learning_fitness = 0.0
        self.testing_fitnesses = [0.0] * len(config.validations)

    def calculate_learning_fitness(self, database: [], chunk) -> float:
        self.learning_fitness = self.learning_simulate(database, chunk)
        return self.learning_fitness

    def calculate_testing_fitness(self, database: [], case) -> float:
        self.testing_fitnesses[case] = self.testing_simulate(database, case)
        return self.testing_fitnesses[case]

    def learning_simulate(self, database: [], chunk) -> float:
        if self.trader.training_wallets[chunk].final:
            return self.trader.training_wallets[chunk].final_value

        day = self.shift_day_by_delta(self.config.start_date)
        while day < self.config.end_date:
            ordered_stocks = sorted(
                database,
                key=lambda stock: self.calculate_strength(stock, day),
                reverse=True,
            )
            self.trader.trade_on_training(ordered_stocks, day, database, chunk)
            day = self.shift_day_by_delta(day)
        return self.trader.get_final_training_fitness(database, chunk)

    def testing_simulate(self, database: [], case):
        if self.trader.testing_wallets[case].final:
            return self.trader.testing_wallets[case].final_value

        (start_date, end_date) = self.config.validations[case]
        day = self.shift_day_by_delta(start_date)
        while day < end_date:
            ordered_stocks = sorted(
                database,
                key=lambda stock: self.calculate_strength(stock, day),
                reverse=True,
            )
            self.trader.trade_on_testing(ordered_stocks, day, database, case)
            day = self.shift_day_by_delta(day)
        return self.trader.get_final_testing_fitness(database, case)

    def calculate_strength(self, stock, day) -> float:
        return sum([g.get_substrength(stock, day) for g in self.genome])

    def to_json_ready(self) -> dict:
        validations_str = [
            f"{self.testing_fitnesses[i]:.2f}"
            for i in range(len(self.testing_fitnesses))
        ]
        genome_str = [g.to_string() for g in self.genome]
        return {
            "id": self.agent_id,
            "strategy": genome_str,
            "fitness": f"{self.learning_fitness:.2f}",
            "validations": validations_str,
        }

    def shift_day_by_delta(self, day: datetime.date) -> datetime.date:
        delta = datetime.timedelta(days=self.config.timedelta)
        day += delta
        return self.shift_to_weekday(day)

    @staticmethod
    def shift_to_weekday(day: datetime.date) -> datetime.date:
        if day.isoweekday() in [6, 7]:
            day += datetime.timedelta(days=8 - day.isoweekday())
        return day
