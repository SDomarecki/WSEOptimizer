import random

from genetic.agent import Agent
from genetic.selection.selection_operator import SelectionOperator


class RouletteSelectionOperator(SelectionOperator):
    def __init__(self, to_save: int):
        super().__init__()
        self.to_save = to_save

    def select(self, agents: [Agent]) -> Agent:
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