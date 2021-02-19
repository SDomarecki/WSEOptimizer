import random

import genetic as g
import genetic.crossover_operators as op


class NonConstant(op.Operator):
    def __init__(self, max_genes: int, to_create: int, validations: []):
        super().__init__()
        self.max_genes = max_genes
        self.to_create = to_create
        self.validations = len(validations)

    def crossover(self, agents: [g.Agent], last_agent_id: int) -> [g.Agent]:
        agent_id = last_agent_id
        offspring = []
        for _ in range(self.to_create):
            parent1 = random.choice(agents)
            parent2 = random.choice(agents)

            child1 = g.Agent(agent_id, 0, self.validations)
            child2 = g.Agent(agent_id + 1, 0, self.validations)

            split1 = random.randint(1, len(parent1.genes) - 1)

            min_for_split2 = max(split1 + len(parent2.genes) - self.max_genes, 1)
            max_for_split2 = min(split1 - len(parent1.genes) + self.max_genes, len(parent2.genes) - 1)

            split2 = random.randint(min_for_split2, max_for_split2)

            child1.genes = parent1.genes[:split1] + parent2.genes[split2:]
            child2.genes = parent2.genes[:split2] + parent1.genes[split1:]

            offspring.append(child1)
            offspring.append(child2)

            agent_id += 2
        return offspring
