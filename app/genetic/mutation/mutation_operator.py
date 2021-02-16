from abc import ABC, abstractmethod

from genetic.agent import Agent


class MutationOperator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def mutate(self, agents: [Agent]) -> [Agent]:
        pass
