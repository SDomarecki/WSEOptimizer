from abc import ABC, abstractmethod

import genetic as g


class Operator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def crossover(self, agents: [g.Agent], last_agent_id: int) -> [g.Agent]:
        pass
