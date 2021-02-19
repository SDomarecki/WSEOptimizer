from abc import ABC, abstractmethod

import genetic as g


class Operator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def select(self, agents: [g.Agent]) -> [g.Agent]:
        pass
