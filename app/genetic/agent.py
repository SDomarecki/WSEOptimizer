import datetime

from app.config import Config
from app.economics.trader import Trader
from app.genetic.genes.gene_factory import GeneFactory


class Agent:
    def __init__(
        self, agent_id, genome_length, gene_factory: GeneFactory, config: Config
    ):
        self.agent_id = agent_id
        self.genes = [gene_factory.create_random_gene() for _ in range(genome_length)]
        self.trader = Trader(config)
        self.config = config
        self.learning_fitness = 0.0
        self.testing_fitnesses = [0.0] * len(config.validations)

    def calculate_learning_fitness(self, database: [], chunk) -> float:
        self.learning_fitness = self.learning_simulate(database, chunk)
        return self.learning_fitness

    def calculate_testing_fitness(
        self, database: [], case, start_date, end_date
    ) -> float:
        self.testing_fitnesses[case] = self.testing_simulate(
            database, case, start_date, end_date
        )
        return self.testing_fitnesses[case]

    def learning_simulate(self, database: [], chunk) -> float:
        if self.trader.training_wallets[chunk].final:
            return self.trader.training_wallets[chunk].final_value

        day = self.next_business_day(self.config.start_date)
        while day < self.config.end_date:
            ordered_stocks = sorted(
                database,
                key=lambda stock: self.calculate_strength(stock, day),
                reverse=True,
            )
            self.trader.trade_on_training(ordered_stocks, day, database, chunk)
            day = self.next_business_day(day)
        return self.trader.get_final_training_fitness(database, chunk)

    def testing_simulate(self, database: [], case, start_date, end_date):
        if self.trader.testing_wallets[case].final:
            return self.trader.testing_wallets[case].final_value

        day = self.next_business_day(start_date)
        while day < end_date:
            ordered_stocks = sorted(
                database,
                key=lambda stock: self.calculate_strength(stock, day),
                reverse=True,
            )
            self.trader.trade_on_testing(ordered_stocks, day, database, case)
            day = self.next_business_day(day)
        return self.trader.get_final_testing_fitness(database, case)

    def calculate_strength(self, stock, day) -> float:
        return sum([g.get_substrength(stock, day) for g in self.genes])

    def to_json_ready(self) -> dict:
        validations_str = [
            f"{self.testing_fitnesses[i]:.2f}"
            for i in range(len(self.testing_fitnesses))
        ]
        genome_str = [g.to_string() for g in self.genes]
        return {
            "id": self.agent_id,
            "strategy": genome_str,
            "fitness": f"{self.learning_fitness:.2f}",
            "validations": validations_str,
        }

    def next_business_day(self, day) -> datetime.date:
        delta = datetime.timedelta(days=self.config.timedelta)
        day += delta
        if day.weekday() == 5:
            day += datetime.timedelta(days=2)
        if day.weekday() == 6:
            day += datetime.timedelta(days=1)
        return day
