from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.genetic.agent import Agent


class Operator(ABC):
    @abstractmethod
    def crossover(self, agents: [Agent], last_agent_id: int) -> [Agent]:
        raise NotImplementedError
