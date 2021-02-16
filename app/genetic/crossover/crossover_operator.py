from abc import ABC, abstractmethod

from genetic.agent import Agent


class CrossoverOperator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def crossover(self, agents: [Agent], last_agent_id: int) -> [Agent]:
        pass
