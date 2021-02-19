import random

import genetic as g
import genetic.selection_operators as op


class Roulette(op.Operator):
    def __init__(self, to_save: int):
        super().__init__()
        self.to_save = to_save

    def select(self, agents: [g.Agent]) -> [g.Agent]:
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
