from app.genetic.genes.gene import Gene


class ImplGene(Gene):
    def __init__(self, left_gene: Gene, right_gene: Gene):
        super().__init__()
        self.leftGene = left_gene
        self.rightGene = right_gene

    def condition(self, company, day):
        # not(a and not b)
        left_cond = self.leftGene.condition(company, day)
        right_cond = self.rightGene.condition(company, day)
        return not left_cond or right_cond

    def condition_to_string(self) -> str:
        return f"IF {self.leftGene.condition_to_string()} THEN {self.rightGene.condition_to_string()}"
