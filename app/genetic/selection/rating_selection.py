from genetic.agent import Agent
from genetic.selection.selection_operator import SelectionOperator


class RatingSelectionOperator(SelectionOperator):
    def __init__(self, to_save: int):
        super().__init__()
        self.to_save = to_save

    def select(self, agents: [Agent]) -> [Agent]:
        sorted_agents = sorted(agents, key=lambda ag: ag.fitness, reverse=True)
        selected = sorted_agents[:int(self.to_save * len(agents))]
        return selected
