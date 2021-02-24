import random

from config import Config
from genetic import crossover_operators
from genetic import mutation_operators
from genetic import selection_operators
from genetic.agent import Agent
from genetic.database_loader import DatabaseLoader
from genetic.genetic_algorithm_worker import GeneticAlgorithmWorker


class GeneticAlgorithmWorkerBuilder:
    def build(self, loader: DatabaseLoader, config: Config) -> GeneticAlgorithmWorker:
        self.config = config
        worker = GeneticAlgorithmWorker(loader, config)

        worker.agents = self.init_agents()
        worker.next_agent_id = self.config.initial_population
        worker.selection_operator = self.init_selection_operator()
        worker.crossover_operator = self.init_crossover_operator()
        worker.mutation_operator = self.init_mutation_operator()
        return worker

    def init_agents(self) -> [Agent]:
        if self.config.constant_length:
            return self.init_constant_length_agents()
        else:
            return self.init_non_constant_length_agents()

    def init_constant_length_agents(self) -> [Agent]:
        return [Agent(i, self.config.initial_length, self.config)
                for i in
                range(self.config.initial_population)]

    def init_non_constant_length_agents(self) -> [Agent]:
        return [Agent(i, random.randint(2, self.config.max_genes), self.config)
                for i in
                range(self.config.initial_population)]

    def init_selection_operator(self) -> selection_operators.Operator:
        method = self.config.selection_method
        if method == 'rating':
            return selection_operators.Rating(self.config.agents_to_save)
        elif method == 'tournament':
            return selection_operators.Tournament(self.config.agents_to_save)
        else:
            return selection_operators.Roulette(self.config.agents_to_save)

    def init_crossover_operator(self) -> crossover_operators.Operator:
        to_create = int((self.config.initial_population - self.config.agents_to_save) / 2)
        if self.config.constant_length:
            return crossover_operators.Constant(self.config.initial_length, to_create,
                                                self.config.validations, self.config)
        else:
            return crossover_operators.NonConstant(self.config.max_genes, to_create,
                                                   self.config.validations, self.config)

    def init_mutation_operator(self) -> mutation_operators.Operator:
        return mutation_operators.Normalization(self.config.mutation_rate)
