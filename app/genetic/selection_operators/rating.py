import genetic as g
import genetic.selection_operators as op


class Rating(op.Operator):
    def __init__(self, to_save: int):
        super().__init__()
        self.to_save = to_save

    def select(self, agents: [g.Agent]) -> [g.Agent]:
        sorted_agents = sorted(agents, key=lambda ag: ag.fitness, reverse=True)
        selected = sorted_agents[:int(self.to_save * len(agents))]
        return selected
