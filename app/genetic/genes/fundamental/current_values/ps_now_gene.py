import random

from app.genetic.genes.fundamental.current_values.gene_current_value import (
    GeneCurrentValue,
)


class PSNowGene(GeneCurrentValue):
    def __init__(self):
        super().__init__()
        self.indicator = "P/S"
        self.denominator_indicator = "SPS"
        self.compared_value = random.uniform(2, 40)
