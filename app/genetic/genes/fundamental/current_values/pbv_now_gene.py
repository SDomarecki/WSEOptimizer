import random

from app.genetic.genes.fundamental.current_values.gene_current_value import (
    GeneCurrentValue,
)


class PBVNowGene(GeneCurrentValue):
    def __init__(self):
        super().__init__()
        self.indicator = "P/BV"
        self.denominator_indicator = "BVPS"
        self.compared_value = random.uniform(0.25, 4)
