from backend.genetic.gene import create_random_gene


class Agent:

    def __init__(self, length):
        self.genes = [create_random_gene() for _ in range(1, length)]
        self.fitness = -1

    def calculate_strength(self, stock, day):
        strength = 0
        for gene in self.genes:
            try:
                strength += gene.get_substrength(stock, day)
            except KeyError:
                continue
        return strength
