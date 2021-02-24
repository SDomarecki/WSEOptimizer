import random

from app.genetic.agent import Agent
from app.genetic.selection_operators import Operator


class Roulette(Operator):
    def __init__(self, to_save: int):
        super().__init__()
        self.to_save = to_save

    def select(self, agents: [Agent]) -> [Agent]:
        selected = []
        selection_target = int(self.to_save * len(agents))
        fitness_sum = sum(agent.fitness for agent in agents)
        while len(selected) < selection_target:
            pick = random.uniform(0, fitness_sum)
            current = 0
            for ag in agents:
                current += ag.fitness
                if current > pick:
                    selected.append(ag)
                    break
        return selected
