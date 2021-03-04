from datetime import date

from app.economics.company import Company
from app.genetic.genes.gene import Gene


class FakeTrueGene(Gene):
    def __init__(self):
        super().__init__()
        self.result_false = -1
        self.result_true = 1
        self.weight = 1.0

    def condition(self, company: Company, day: date) -> bool:
        return True

    def condition_to_string(self) -> str:
        return "Fake"
