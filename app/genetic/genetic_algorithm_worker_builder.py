import random

from app.config import Config

from app.genetic.agent import Agent
from app.genetic.benchmark_agent import BenchmarkAgent
from app.genetic.database_loader import DatabaseLoader
from app.genetic.genetic_algorithm_worker import GeneticAlgorithmWorker
from app.genetic.genes.gene_factory import GeneFactory
from app.genetic.reporting.plotter import Plotter
from app.genetic.selection_operators.operator import Operator as SelectionOperator
from app.genetic.crossover_operators.operator import Operator as CrossoverOperator
from app.genetic.mutation_operators.operator import Operator as MutationOperator
from app.genetic.crossover_operators.constant import Constant
from app.genetic.crossover_operators.non_constant import NonConstant
from app.genetic.mutation_operators.normalization import Normalization
from app.genetic.selection_operators.rating import Rating
from app.genetic.selection_operators.roulette import Roulette
from app.genetic.selection_operators.tournament import Tournament


class GeneticAlgorithmWorkerBuilder:
    def __init__(self):
        self.config = None
        self.gene_factory = None

    def build(self, loader: DatabaseLoader, config: Config) -> GeneticAlgorithmWorker:
        self.config = config
        self.gene_factory = GeneFactory(config)
        worker = GeneticAlgorithmWorker(config)

        worker.agents = self.init_agents()
        worker.benchmark_agent = self.init_benchmark_agent()
        worker.next_agent_id = self.config.initial_population
        worker.selection_operator = self.init_selection_operator()
        worker.crossover_operator = self.init_crossover_operator()
        worker.mutation_operator = self.init_mutation_operator()

        worker.learning_database = loader.learning_database
        worker.testing_databases = loader.testing_databases
        worker.chunk_size = int(
            len(loader.learning_database.companies) / self.config.chunks
        )
        worker.plotter = Plotter(config)
        return worker

    def init_agents(self) -> [Agent]:
        if self.config.constant_length:
            return self.init_constant_length_agents()
        return self.init_non_constant_length_agents()

    def init_benchmark_agent(self) -> [BenchmarkAgent]:
        return BenchmarkAgent(self.config)

    def init_constant_length_agents(self) -> [Agent]:
        agents = []
        for i in range(self.config.initial_population):
            genome = self.gene_factory.create_n_random_genes(self.config.initial_length)
            agents.append(Agent(i, genome, self.config))
        return agents

    def init_non_constant_length_agents(self) -> [Agent]:
        agents = []
        for i in range(self.config.initial_population):
            genome_length = random.randint(2, self.config.max_genes)
            genome = self.gene_factory.create_n_random_genes(genome_length)
            agents += Agent(i, genome, self.config)
        return agents

    def init_selection_operator(self) -> SelectionOperator:
        method = self.config.selection_method
        if method == "rating":
            return Rating(self.config.agents_to_save)
        if method == "tournament":
            return Tournament(self.config.agents_to_save)
        return Roulette(self.config.agents_to_save)

    def init_crossover_operator(self) -> CrossoverOperator:
        to_create = int(
            (self.config.initial_population - self.config.agents_to_save) / 2
        )
        if self.config.constant_length:
            return Constant(
                self.config.initial_length,
                to_create,
                self.config,
            )
        return NonConstant(
            self.config.max_genes,
            to_create,
            self.config,
        )

    def init_mutation_operator(self) -> MutationOperator:
        return Normalization(self.config.mutation_rate)
