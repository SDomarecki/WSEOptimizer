from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import app.genetic as g


class Operator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def crossover(self, agents: [g.Agent], last_agent_id: int) -> [g.Agent]:
        pass
