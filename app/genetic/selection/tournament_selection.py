import random

from genetic.agent import Agent
from genetic.selection.selection_operator import SelectionOperator


class TournamentSelectionOperator(SelectionOperator):
    def __init__(self, to_save: int):
        super().__init__()
        self.to_save = to_save

    def select(self, agents: [Agent]) -> [Agent]:
        selected = []
        selection_target = int(self.to_save * len(agents))
        tournament_size = 2
        while len(selected) < selection_target:
            aspirants = [random.choice(agents) for _ in range(tournament_size)]
            selected.append(max(aspirants, key=lambda ag: ag.fitness))
        return selected
