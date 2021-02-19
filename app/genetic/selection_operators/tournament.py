import random

import genetic as g
import genetic.selection_operators as op


class Tournament(op.Operator):
    def __init__(self, to_save: int):
        super().__init__()
        self.to_save = to_save

    def select(self, agents: [g.Agent]) -> [g.Agent]:
        selected = []
        selection_target = int(self.to_save * len(agents))
        tournament_size = 2
        while len(selected) < selection_target:
            aspirants = [random.choice(agents) for _ in range(tournament_size)]
            selected.append(max(aspirants, key=lambda ag: ag.fitness))
        return selected
