import random

from app.genetic.genes.fundamental.statement_values.gene_statement_value import (
    GeneStatementValue,
)


class PBVGene(GeneStatementValue):
    def __init__(self):
        super().__init__()
        self.indicator = "P/BV"
        self.compared_value = random.uniform(0.25, 4)
