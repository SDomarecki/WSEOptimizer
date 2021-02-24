from abc import ABC, abstractmethod

from genetic.agent import Agent


class Operator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def select(self, agents: [Agent]) -> [Agent]:
        pass
