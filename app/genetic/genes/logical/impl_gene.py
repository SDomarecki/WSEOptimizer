from ..gene import Gene
from ..gene_factory import GeneFactory


class ImplGene(Gene):

    def __init__(self, factory: GeneFactory):
        super().__init__()
        self.leftGene = factory.create_non_logic_gene()
        self.rightGene = factory.create_non_logic_gene()

    def condition(self, company, day):
        # not(not a and b)
        return self.leftGene.condition(company, day) or not self.rightGene.condition(company, day)

    def condition_to_string(self) -> str:
        return f'({self.leftGene.condition_to_string()} THEN {self.rightGene.condition_to_string()}'
