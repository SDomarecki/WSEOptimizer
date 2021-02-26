from __future__ import annotations

from app.genetic.genes import Gene

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.genetic.genes import GeneFactory


class EqGene(Gene):
    def __init__(self, factory: GeneFactory):
        super().__init__()
        self.leftGene = factory.create_non_logic_gene()
        self.rightGene = factory.create_non_logic_gene()

    def condition(self, company, day):
        return self.leftGene.condition(company, day) == self.rightGene.condition(
            company, day
        )

    def condition_to_string(self) -> str:
        return f"({self.leftGene.condition_to_string()} EQUALS {self.rightGene.condition_to_string()}"
