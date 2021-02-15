from genes.gene_factory import GeneFactory

from app.genetic.genes.gene import Gene


class XorGene(Gene):

    def __init__(self):
        super().__init__()
        self.leftGene = GeneFactory.create_non_logic_gene()
        self.rightGene = GeneFactory.create_non_logic_gene()

    def condition(self, company, day):
        left_cond = self.leftGene.condition(company, day)
        right_cond = self.rightGene.condition(company, day)
        return (left_cond or right_cond) and not (left_cond and right_cond)

    def condition_to_string(self):
        return "(" + self.leftGene.condition_to_string() + " XOR " + self.rightGene.condition_to_string() + ")"
