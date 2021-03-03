from app.genetic.genes.gene import Gene


class EqGene(Gene):
    def __init__(self, left_gene: Gene, right_gene: Gene):
        super().__init__()
        self.leftGene = left_gene
        self.rightGene = right_gene

    def condition(self, company, day):
        left_cond = self.leftGene.condition(company, day)
        right_cond = self.rightGene.condition(company, day)
        return left_cond == right_cond

    def condition_to_string(self) -> str:
        return f"{self.leftGene.condition_to_string()} EQUALS {self.rightGene.condition_to_string()}"
