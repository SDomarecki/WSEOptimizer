from __future__ import annotations

from app.genetic.genes.gene import Gene

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.genetic.genes.gene_factory import GeneFactory


class XorGene(Gene):
    def __init__(self, factory: GeneFactory):
        super().__init__()
        self.leftGene = factory.create_non_logic_gene()
        self.rightGene = factory.create_non_logic_gene()

    def condition(self, company, day):
        left_cond = self.leftGene.condition(company, day)
        right_cond = self.rightGene.condition(company, day)
        return (left_cond or right_cond) and not (left_cond and right_cond)

    def condition_to_string(self) -> str:
        return f"({self.leftGene.condition_to_string()} XOR {self.rightGene.condition_to_string()}"
