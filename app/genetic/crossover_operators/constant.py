import random

import genetic as g
import genetic.crossover_operators as op


class Constant(op.Operator):
    def __init__(self, agent_len: int, to_create: int, validations: []):
        super().__init__()
        self.agent_len = agent_len
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

            split = random.randint(0, self.agent_len)
            child1.genes = parent1.genes[:split] + parent2.genes[split:]
            child2.genes = parent2.genes[:split] + parent1.genes[split:]

            offspring.append(child1)
            offspring.append(child2)

            agent_id += 2
        return offspring
