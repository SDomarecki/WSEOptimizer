import random

from app.genetic.genes.fundamental.statement_values.gene_statement_value import (
    GeneStatementValue,
)


class PSGene(GeneStatementValue):
    def __init__(self):
        super().__init__()
        self.indicator = "P/S"
        self.compared_value = random.uniform(2, 40)
