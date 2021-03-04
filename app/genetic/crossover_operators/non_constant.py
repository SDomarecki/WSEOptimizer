import random

from app.config import Config
from app.genetic.agent import Agent
from app.genetic.crossover_operators.operator import Operator


class NonConstant(Operator):
    def __init__(
        self,
        max_genes: int,
        to_create: int,
        config: Config,
    ):
        super().__init__()
        self.max_genes = max_genes
        self.to_create = to_create
        self.config = config

    def crossover(self, agents: [Agent], last_agent_id: int) -> [Agent]:
        agent_id = last_agent_id
        offspring = []
        for _ in range(self.to_create):
            [parent1, parent2] = random.sample(agents, 2)

            split1 = random.randint(1, len(parent1.genome) - 1)

            min_for_split2 = max(split1 + len(parent2.genome) - self.max_genes, 1)
            max_for_split2 = min(
                split1 - len(parent1.genome) + self.max_genes, len(parent2.genome) - 1
            )

            split2 = random.randint(min_for_split2, max_for_split2)

            child1_genome = parent1.genome[:split1] + parent2.genome[split2:]
            child2_genome = parent2.genome[:split2] + parent1.genome[split1:]

            child1 = Agent(agent_id, child1_genome, self.config)
            child2 = Agent(agent_id + 1, child2_genome, self.config)

            offspring.append(child1)
            offspring.append(child2)

            agent_id += 2
        return offspring
