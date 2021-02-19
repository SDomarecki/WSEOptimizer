import random

import genetic as g
import genetic.genes as genes
import genetic.mutation_operators as op


class GeneCreation(op.Operator):
    def __init__(self, mutation_rate: float, factory: genes.GeneFactory):
        super().__init__()
        self.mutation_rate = mutation_rate
        self.factory = factory

    def mutate(self, agents: [g.Agent]) -> [g.Agent]:
        for agent in agents:
            for idx, param in enumerate(agent.genes):
                if random.uniform(0.0, 1.0) <= self.mutation_rate:
                    agent.genes[idx] = self.factory.create_random_gene()
        return agents
