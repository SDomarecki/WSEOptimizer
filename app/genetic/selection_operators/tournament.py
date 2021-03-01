import random

from app.genetic.agent import Agent
from app.genetic.selection_operators.operator import Operator


class Tournament(Operator):
    def __init__(self, to_save_rate: float):
        super().__init__()
        self.to_save_rate = to_save_rate

    def select(self, agents: [Agent]) -> [Agent]:
        selection_target_amount = int(self.to_save_rate * len(agents))
        tournament_size = 2
        selected = [
            self.select_one_aspirant(agents, tournament_size)
            for _ in range(selection_target_amount)
        ]
        return selected

    def select_one_aspirant(self, agents: [Agent], tournament_size: int) -> Agent:
        aspirants = random.sample(agents, tournament_size)
        return max(aspirants, key=lambda ag: ag.learning_fitness)
