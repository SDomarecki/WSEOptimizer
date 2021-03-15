import random

from app.genetic.genes.fundamental.statement_values.gene_statement_value import (
    GeneStatementValue,
)


class ROAGene(GeneStatementValue):
    def __init__(self):
        super().__init__()
        self.indicator = "ROA"
        self.compared_value = random.uniform(-0.5, 0.5)
