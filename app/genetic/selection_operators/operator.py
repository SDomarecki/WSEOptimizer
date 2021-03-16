from abc import ABC, abstractmethod

from app.genetic.agent import Agent


class Operator(ABC):
    @abstractmethod
    def select(self, agents: [Agent]) -> [Agent]:
        raise NotImplementedError
