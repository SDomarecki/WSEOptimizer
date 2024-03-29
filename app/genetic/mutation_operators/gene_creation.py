from app.genetic.mutation_operators.operator import Operator
from app.genetic.genes.gene import Gene
from app.genetic.genes.gene_factory import GeneFactory


class GeneCreation(Operator):
    def __init__(self, mutation_rate: float, factory: GeneFactory):
        super().__init__(mutation_rate)
        self.factory = factory

    def mutate_one_gene(self, gene) -> Gene:
        return self.factory.create_random_gene()
