from datetime import date

from app.economics.company import Company
from app.genetic.genes.gene import Gene


class FakeTrueGene(Gene):
    def condition(self, company: Company, day: date) -> bool:
        return True

    def condition_to_string(self) -> str:
        return "Fake"
