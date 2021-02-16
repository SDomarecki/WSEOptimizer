import random

from genetic.agent import Agent
from genetic.mutation.mutation_operator import MutationOperator


class NormalizationMutationOperator(MutationOperator):
    def __init__(self, mutation_rate: float):
        super().__init__()
        self.mutation_rate = mutation_rate

    def mutate(self, agents: [Agent]) -> [Agent]:
        for agent in agents:
            for idx, param in enumerate(agent.genes):
                if random.uniform(0.0, 1.0) <= self.mutation_rate:
                    agent.genes[idx].weight = random.uniform(0.0, 1.0)
                    # Normal mode
                    # from genes.gene_factory import GeneFactory
                    # agent.genes[idx] = GeneFactory.create_random_gene()
        return agents
