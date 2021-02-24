import random

from app.genetic.agent import Agent
from app.genetic.mutation_operators import Operator


class Normalization(Operator):
    def __init__(self, mutation_rate: float):
        super().__init__()
        self.mutation_rate = mutation_rate

    def mutate(self, agents: [Agent]) -> [Agent]:
        for agent in agents:
            for idx, param in enumerate(agent.genes):
                if random.uniform(0.0, 1.0) <= self.mutation_rate:
                    agent.genes[idx].weight = random.uniform(0.0, 1.0)
        return agents
