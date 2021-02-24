import datetime

from app.config import Config
from app.economics.wallet import Wallet
from app.genetic.genes import GeneFactory


class Agent:

    def __init__(self, id, genome_length, gene_factory: GeneFactory, config: Config):
        self.id = id
        self.genes = [gene_factory.create_random_gene() for _ in range(genome_length)]
        self.fitness = 0.0
        self.validations = [0.0] * len(config.validations)
        self.wallet = None
        self.config = config

    # validation_case = -1 -> learning
    def calculate_fitness(self, database, start, end, validation_case=-1) -> float:
        self.wallet = Wallet(self.config)
        simulation_result = self.simulate(database, start, end)

        if validation_case == -1:
            self.fitness = simulation_result
        else:
            self.validations[validation_case] = simulation_result

        return simulation_result

    def simulate(self, database, start_date, end_date) -> float:
        day = start_date
        delta = datetime.timedelta(days=self.config.timedelta)
        while day < end_date:
            if day.weekday() == 5:
                day += datetime.timedelta(days=2)
            if day.weekday() == 6:
                day += datetime.timedelta(days=1)

            ordered_stocks = sorted(database.values(), key=lambda s: self.calculate_strength(s, day), reverse=True)
            self.wallet.trade(ordered_stocks, day, database)
            day += delta

        if self.config.return_method == 'total_value':
            return self.wallet.get_total_value(database, end_date)
        elif self.config.return_method == 'sharpe':
            return self.wallet.get_current_sharpe(database, end_date)

    def calculate_strength(self, stock, day) -> float:
        return sum([g.get_substrength(stock, day) for g in self.genes])

    def to_json_ready(self) -> dict:
        validations_str = [f'{self.validations[i]:.2f}' for i in range(len(self.validations))]
        return {
            'id': self.id,
            'strategy': self.genome_to_string(),
            'fitness': f'{self.fitness:.2f}',
            'validations': validations_str
        }

    def genome_to_string(self) -> [str]:
        return [g.to_string() for g in self.genes]
