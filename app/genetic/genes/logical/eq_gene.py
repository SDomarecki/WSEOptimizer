from genes.gene_factory import GeneFactory

from app.genetic.genes.gene import Gene


class EqGene(Gene):

    def __init__(self):
        super().__init__()
        self.leftGene = GeneFactory.create_non_logic_gene()
        self.rightGene = GeneFactory.create_non_logic_gene()

    def condition(self, company, day):
        return self.leftGene.condition(company, day) == self.rightGene.condition(company, day)

    def condition_to_string(self):
        return "(" + self.leftGene.condition_to_string() + " THEN " + self.rightGene.condition_to_string() + ")"
