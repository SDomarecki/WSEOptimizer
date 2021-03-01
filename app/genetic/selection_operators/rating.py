from app.genetic.agent import Agent
from app.genetic.selection_operators.operator import Operator


class Rating(Operator):
    def __init__(self, to_save_rate: float):
        super().__init__()
        self.to_save_rate = to_save_rate

    def select(self, agents: [Agent]) -> [Agent]:
        selection_target_amount = int(self.to_save_rate * len(agents))
        sorted_agents = sorted(agents, key=lambda ag: ag.learning_fitness, reverse=True)
        selected = sorted_agents[:selection_target_amount]
        return selected
