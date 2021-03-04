import random

from app.config import Config
from app.genetic.agent import Agent
from app.genetic.crossover_operators.operator import Operator


class NonConstant(Operator):
    def __init__(
        self,
        max_genes: int,
        to_create: int,
        validations: [],
        config: Config,
    ):
        super().__init__()
        self.max_genes = max_genes
        self.to_create = to_create
        self.validations = len(validations)
        self.config = config

    def crossover(self, agents: [Agent], last_agent_id: int) -> [Agent]:
        agent_id = last_agent_id
        offspring = []
        for _ in range(self.to_create):
            parent1 = random.choice(agents)
            parent2 = random.choice(agents)

            split1 = random.randint(1, len(parent1.genes) - 1)

            min_for_split2 = max(split1 + len(parent2.genes) - self.max_genes, 1)
            max_for_split2 = min(
                split1 - len(parent1.genes) + self.max_genes, len(parent2.genes) - 1
            )

            split2 = random.randint(min_for_split2, max_for_split2)

            child1_genes = parent1.genes[:split1] + parent2.genes[split2:]
            child2_genes = parent2.genes[:split2] + parent1.genes[split1:]

            child1 = Agent(agent_id, child1_genes, self.config)
            child2 = Agent(agent_id + 1, child2_genes, self.config)

            offspring.append(child1)
            offspring.append(child2)

            agent_id += 2
        return offspring
