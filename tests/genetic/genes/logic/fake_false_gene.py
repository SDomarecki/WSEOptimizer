from datetime import date

from app.economics.company import Company
from app.genetic.genes.gene import Gene


class FakeFalseGene(Gene):
    def condition(self, company: Company, day: date) -> bool:
        return False

    def condition_to_string(self) -> str:
        return "Fake"
