import random
from datetime import date

from app.economics.company import Company

from abc import ABC, abstractmethod


class Gene(ABC):
    def __init__(self):
        self.result_true = random.randint(1, 10) * random.choice([-1, 1])
        self.result_false = random.randint(1, 10) * random.choice([-1, 1])
        while self.result_false == self.result_true:
            self.result_false = random.randint(1, 10) * random.choice([-1, 1])
        self.weight = round(random.uniform(0.0, 1.0), 2)

    def get_substrength(self, company: Company, day: date) -> float:
        try:
            if self.condition(company, day):
                return self.weight * self.result_true
            return self.weight * self.result_false
        except KeyError:
            return 0.0

    def to_string(self) -> str:
        return f"{self.weight:.2f} x If({self.condition_to_string()}) then {self.result_true} else {self.result_false}"

    @abstractmethod
    def condition(self, company: Company, day: date) -> bool:
        raise NotImplementedError

    @abstractmethod
    def condition_to_string(self) -> str:
        raise NotImplementedError
