import random

from app.genetic.mutation_operators.operator import Operator
from app.genetic.genes.gene import Gene


class Normalization(Operator):
    def mutate_one_gene(self, gene: Gene) -> Gene:
        new_gene = gene
        new_gene.weight = random.uniform(0.0, 1.0)
        return new_gene
