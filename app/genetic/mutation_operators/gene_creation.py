import random

from genetic.agent import Agent
from genetic.genes import GeneFactory
from genetic.mutation_operators import Operator


class GeneCreation(Operator):
    def __init__(self, mutation_rate: float, factory: GeneFactory):
        super().__init__()
        self.mutation_rate = mutation_rate
        self.factory = factory

    def mutate(self, agents: [Agent]) -> [Agent]:
        for agent in agents:
            for idx, param in enumerate(agent.genes):
                if random.uniform(0.0, 1.0) <= self.mutation_rate:
                    agent.genes[idx] = self.factory.create_random_gene()
        return agents
