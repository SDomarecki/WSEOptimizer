import random

import genetic as g
import genetic.mutation_operators as op


class Normalization(op.Operator):
    def __init__(self, mutation_rate: float):
        super().__init__()
        self.mutation_rate = mutation_rate

    def mutate(self, agents: [g.Agent]) -> [g.Agent]:
        for agent in agents:
            for idx, param in enumerate(agent.genes):
                if random.uniform(0.0, 1.0) <= self.mutation_rate:
                    agent.genes[idx].weight = random.uniform(0.0, 1.0)
        return agents
