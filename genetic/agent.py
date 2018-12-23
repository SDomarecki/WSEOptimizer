import datetime

from genetic.genes.gene_factory import GeneFactory
from genetic.wallet import Wallet
from shared.config import Config


class Agent:

    def __init__(self, id, length, validation_length):
        self.id = id
        self.genes = [GeneFactory.create_random_gene() for _ in range(length)]
        self.fitness = 0.0
        self.validations = [0.0] * validation_length
        self.wallet = None

    # validation_case = -1 -> learning
    def calculate_fitness(self, database, start, end, validation_case=-1) -> float:
        self.wallet = Wallet()
        simulation_result = self.simulate(database, start, end)

        if validation_case == -1:
            self.fitness = simulation_result
        else:
            self.validations[validation_case] = simulation_result

        return simulation_result

    def simulate(self, database, start_date, end_date) -> float:
        day = start_date
        delta = datetime.timedelta(days=Config.timedelta)
        while day < end_date:
            if day.weekday() == 5:
                day += datetime.timedelta(days=2)
            if day.weekday() == 6:
                day += datetime.timedelta(days=1)

            ordered_stocks = sorted(database.values(), key=lambda s: self.calculate_strength(s, day), reverse=True)
            self.wallet.trade(ordered_stocks, day, database)
            day += delta

        if Config.return_method == "total_value":
            return self.wallet.get_total_value(database, end_date)
        elif Config.return_method == "sharpe":
            return self.wallet.get_current_sharpe(database, end_date)

    def calculate_strength(self, stock, day) -> float:
        return sum([g.get_substrength(stock, day) for g in self.genes])

    def to_json_ready(self):
        validations_str = ["{0:.2f}".format(self.validations[i]) for i in range(len(self.validations))]
        return {
            "id": self.id,
            "strategy": self.genome_to_string(),
            "fitness": "{0:.2f}".format(self.fitness),
            "validations": validations_str
        }

    def genome_to_string(self) -> [str]:
        return [g.to_string() for g in self.genes]
