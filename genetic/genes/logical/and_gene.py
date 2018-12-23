from genes.gene_factory import GeneFactory
from genetic.genes.gene import Gene


class AndGene(Gene):

    def __init__(self):
        super().__init__()
        self.leftGene = GeneFactory.create_non_logic_gene()
        self.rightGene = GeneFactory.create_non_logic_gene()

    def condition(self, company, day):
        return self.leftGene.condition(company, day) and self.rightGene.condition(company, day)

    def condition_to_string(self):
        return "(" + self.leftGene.condition_to_string() + " AND " + self.rightGene.condition_to_string() + ")"