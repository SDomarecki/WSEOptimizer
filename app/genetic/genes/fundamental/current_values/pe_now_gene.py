import random

from app.genetic.genes.fundamental.current_values.gene_current_value import (
    GeneCurrentValue,
)


class PENowGene(GeneCurrentValue):
    def __init__(self):
        super().__init__()
        self.indicator = "P/E"
        self.denominator_indicator = "EPS"
        self.compared_value = random.uniform(2, 40)
