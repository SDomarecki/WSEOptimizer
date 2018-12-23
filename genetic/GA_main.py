import random

from database_loader import DatabaseLoader
from genetic.agent import Agent
from shared.config import Config


class GeneticAlgorithmWorker:

    def __init__(self):
        loader = DatabaseLoader('../res', Config.benchmark)

        self.next_agent_id = 1
        self.learning_database = loader.learning_database
        self.learning_database_chunks = loader.learning_database_chunks
        self.testing_database = loader.testing_databases
        self.agents = []
        self.generations = Config.iterations
        self.targets = loader.targets
        self.best_scores = []

        self.init_agents()

    def init_agents(self):
        if Config.constant_length:
            self.agents = [Agent(self.next_agent_id + i, Config.initial_length, len(Config.validations))
                           for i in
                           range(Config.initial_population)]
        else:
            self.agents = [Agent(self.next_agent_id + i, random.randint(2, Config.max_genes), len(Config.validations))
                           for i in
                           range(Config.initial_population)]
        self.next_agent_id += Config.initial_population

    def perform_ga(self):
        print('Learning database size: %s companies' % len(self.learning_database))

        chunks = Config.chunks

        for generation in range(1, self.generations):
            current_database = self.learning_database_chunks[generation % chunks]

            print('Generation: %s' % generation)

            for agent in self.agents:
                fit = agent.calculate_fitness(current_database, Config.start_date, Config.end_date)
                print('[%s] fitness - %s' % (agent.id, fit))
            self.selection()

            if generation < self.generations - 1:
                self.crossover()
            self.print_best_agent_performance(generation)

        # Iteration with whole database
        print('Last generation')
        for agent in self.agents:
            fit = agent.calculate_fitness(self.learning_database, Config.start_date, Config.end_date)
            print('[%s] fitness - %s' % (agent.id, fit))
        self.agents = sorted(self.agents, key=lambda ag: ag.fitness, reverse=True)

    # funkcja sortująca i niszcząca słabe osobniki
    def selection(self):
        self.agents = sorted(self.agents, key=lambda ag: ag.fitness, reverse=True)
        self.agents = self.agents[:int(Config.agents_to_save * len(self.agents))]

    # funkcja tworząca nowe osobniki
    def crossover(self):
        if Config.constant_length:
            self.constant_crossover()
        else:
            self.non_constant_crossover()

    def constant_crossover(self):
        to_create = int((Config.initial_population - len(self.agents)) /2)

        offspring = []

        for _ in range(to_create):
            parent1 = random.choice(self.agents)
            parent2 = random.choice(self.agents)

            child1 = Agent(self.next_agent_id, 0, len(Config.validations))
            child2 = Agent(self.next_agent_id + 1, 0, len(Config.validations))

            split = random.randint(0, Config.initial_length)
            child1.genes = parent1.genes[:split] + parent2.genes[split:]
            child2.genes = parent2.genes[:split] + parent1.genes[split:]

            offspring.append(child1)
            offspring.append(child2)

            self.next_agent_id += 2

        offspring = self.mutation(offspring)
        self.agents.extend(offspring)

    def non_constant_crossover(self):
        to_create = int((Config.initial_population - len(self.agents)) / 2)

        offspring = []
        for _ in range(to_create):
            parent1 = random.choice(self.agents)
            parent2 = random.choice(self.agents)

            child1 = Agent(self.next_agent_id, 0, len(Config.validations))
            child2 = Agent(self.next_agent_id + 1, 0, len(Config.validations))

            split1 = random.randint(1, len(parent1.genes) - 1)

            min_for_split2 = max(split1 + len(parent2.genes) - Config.max_genes, 1)
            max_for_split2 = min(split1 - len(parent1.genes) + Config.max_genes, len(parent2.genes) - 1)

            split2 = random.randint(min_for_split2, max_for_split2)

            child1.genes = parent1.genes[:split1] + parent2.genes[split2:]
            child2.genes = parent2.genes[:split2] + parent1.genes[split1:]

            offspring.append(child1)
            offspring.append(child2)

            self.next_agent_id += 2

        offspring = self.mutation(offspring)
        self.agents.extend(offspring)

    # funkcja podmieniająca geny w nowych osobnikach
    def mutation(self, agents: [Agent]) -> [Agent]:
        import random
        for agent in agents:
            for idx, param in enumerate(agent.genes):
                if random.uniform(0.0, 1.0) <= Config.mutation_rate:
                    # Szwed mode
                    agent.genes[idx].weight = random.uniform(0.0, 1.0)
                    # Normal mode
                    # from genes.gene_factory import GeneFactory
                    # agent.genes[idx] = GeneFactory.create_random_gene()
        return agents

    def print_best_agent_performance(self, generation):
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt

        best_agent = max(self.agents, key=lambda ag: ag.fitness)
        for idx, validation in enumerate(Config.validations):
            fit = best_agent.calculate_fitness(self.testing_database[idx], validation[0], validation[1], validation_case=idx)
            print('[%s] validation #%s - %s' % (best_agent.id, idx, fit))

            self.best_scores.append(best_agent.validations[0])
            x = mdates.date2num(best_agent.wallet.valueTimestamps)
            y = best_agent.wallet.valueHistory
            plt.xticks(rotation=45)
            plt.gcf().subplots_adjust(bottom=0.15)
            plt.hlines(self.targets[idx],
                       xmin=validation[0],
                       xmax=validation[1],
                       color='r',
                       linestyle='--')
            plt.plot_date(x, y, '-g')

            plt.savefig('../' + str(generation) + '_' + str(idx) + '.png', dpi=500)
            plt.close()

            plt.plot(self.best_scores)
            plt.axhline(self.targets[idx],
                        color='r',
                        linestyle='--')
            plt.show()
            plt.close()

        print('Best agent performance')
        print('Learning: ' + str(best_agent.fitness))
        print('Validations: ')
        for val in best_agent.validations:
            print(str(val))
        print('Length of genome: ' + str(len(best_agent.genes)))

    def save_results(self, save_path: str):
        self.calculate_all_validations()
        result_string = self.toJSON()
        self.save_to_file(result_string, save_path)

    def calculate_all_validations(self):
        for _, agent in enumerate(self.agents[:5]):
            for val_idx, validation in enumerate(Config.validations):
                fit = agent.calculate_fitness(self.testing_database[val_idx], validation[0], validation[1], validation_case=val_idx)
                print('[%s] validation #%s - %s' % (agent.id, val_idx, fit))
        self.best_scores.append(self.agents[0].validations[0])

    def save_to_file(self, result: str, save_path: str):
        file = open(save_path, 'w')
        file.write(result)
        file.close()

        import matplotlib.pyplot as plt
        plt.plot(self.best_scores)
        plt.axhline(self.targets[0],
                    color='r',
                    linestyle='--')
        plt.show()

    class JSONPack:
        def __init__(self, agents, targets):
            self.timestamp = strftime("%Y-%m-%d %H-%M-%S", localtime())
            self.fitness_start = Config.start_date
            self.fitness_end = Config.end_date

            self.validations = []
            for idx, target in enumerate(targets):
                self.validations.append({
                    "start_date": Config.validations[idx][0],
                    "end_date": Config.validations[idx][1],
                    "target": target
                })
            self.start_cash = Config.start_cash
            self.agents = list(map(lambda ag: ag.to_json_ready(), agents))

    def toJSON(self):
        import json
        return json.dumps(self.JSONPack(self.agents[:5], self.targets).__dict__, default=str, indent=2)


if __name__ == "__main__":
    Config()
    worker = GeneticAlgorithmWorker()
    worker.perform_ga()

    from time import strftime, localtime

    filename = strftime("%Y-%m-%d %H-%M-%S", localtime())

    worker.save_results('../' + filename + '.json')
