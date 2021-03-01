import random

from app.genetic.agent import Agent
from app.genetic.selection_operators.operator import Operator


class Roulette(Operator):
    def __init__(self, to_save_rate: float):
        super().__init__()
        self.to_save_rate = to_save_rate
        self.fitness_sum = 0.0

    def select(self, agents: [Agent]) -> [Agent]:
        selected = []
        selection_target = int(self.to_save_rate * len(agents))
        self.fitness_sum = sum(agent.learning_fitness for agent in agents)
        while len(selected) < selection_target:
            pick = random.uniform(0, self.fitness_sum)
            current = 0
            for ag in agents:
                current += ag.learning_fitness
                if current > pick:
                    selected.append(ag)
                    break
        return selected
