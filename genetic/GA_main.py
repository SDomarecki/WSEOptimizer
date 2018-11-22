from genetic.agent import Agent
from genetic.database_loader import read_database, get_target_ratio
from shared.config import Config
from shared.config import read_config


class GA:

    def __init__(self):
        self.next_agent_id = 1
        self.database = read_database(path_to_database='../res')
        self.agents = [Agent(self.next_agent_id + i, Config.initial_length) for i in range(Config.initial_population)]
        self.next_agent_id += Config.initial_population
        self.generations = Config.iterations

        self.target = Config.start_cash * \
                      get_target_ratio(Config.benchmark,
                                       Config.validation_start_date,
                                       Config.validation_end_date,
                                       path_to_database='../res')
        print('Validation target: ' + str(self.target))

    def perform_ga(self):
        print("Database size: " + str(len(self.database)) + " companies")

        chunks = 3
        database_chunks = self.split_database_equally(chunks=chunks)

        for generation in range(1, self.generations+1):
            current_database = database_chunks[generation % chunks]

            print('Generation: ' + str(generation))

            for agent in self.agents:
                agent.calculate_fitness(current_database)

            if generation < self.generations - 1:
                self.selection()
                to_create = int((Config.initial_population - len(self.agents)) / 2)
                self.crossover(to_create)

                self.print_best_agent_performance()

        # Iteration with whole database
        print('Last generation')
        for agent in self.agents:
            agent.calculate_fitness(self.database)
        self.agents = sorted(self.agents, key=lambda ag: ag.fitness, reverse=True)

    # fukcja sortująca i niszcząca słabe osobniki
    def selection(self):
        self.agents = sorted(self.agents, key=lambda ag: ag.fitness, reverse=True)
        self.agents = self.agents[:int(Config.agents_to_drop * len(self.agents))]

    # fukcja tworząca nowe osobniki
    def crossover(self, to_create: int):
        import random

        offspring = []

        for _ in range(to_create):
            parent1 = random.choice(self.agents)
            parent2 = random.choice(self.agents)
            child1 = Agent(self.next_agent_id, 1)
            child2 = Agent(self.next_agent_id + 1, 1)
            split = random.randint(0, Config.initial_length)
            child1.genes = parent1.genes[0:split] + parent2.genes[split:Config.initial_length]
            child2.genes = parent2.genes[0:split] + parent1.genes[split:Config.initial_length]

            child1.weights = parent1.weights[0:split] + parent2.weights[split:Config.initial_length]
            child2.weights = parent2.weights[0:split] + parent1.weights[split:Config.initial_length]

            offspring.append(child1)
            offspring.append(child2)

            self.next_agent_id += 2

        offspring = self.mutation(offspring)
        self.agents.extend(offspring)

    # funkcja podmieniająca wagi genów w nowych osobnikach
    def mutation(self, agents: [Agent]) -> [Agent]:
        import random
        for agent in agents:
            for idx, param in enumerate(agent.genes):
                if random.uniform(0.0, 1.0) <= 0.3:
                    agent.weights[idx] = random.uniform(0.0, 1.0)
        return agents

    def print_best_agent_performance(self):
        best_agent = max(self.agents, key=lambda ag: ag.fitness)
        best_agent.calculate_fitness(self.database, validation=True)
        print('Best agent performance')
        print('Learning:: ' + str(best_agent.fitness))
        print('Validation: ' + str(best_agent.validation))

    def split_database_equally(self, chunks=2):
        "Splits dict by keys. Returns a list of dictionaries."
        # prep with empty dicts
        return_list = [dict() for _ in range(chunks)]
        idx = 0
        for k, v in self.database.items():
            return_list[idx][k] = v
            if idx < chunks - 1:  # indexes start at 0
                idx += 1
            else:
                idx = 0
        return return_list

    def save_results(self, save_path: str):
        result_string = self.get_result_string()
        self.save_to_file(result_string, save_path)

    def get_result_string(self) -> str:
        for counter, value in enumerate(self.agents[:5]):
            value.calculate_fitness(self.database, validation=True)
        return self.toJSON()

    def save_to_file(self, result: str, save_path: str):
        file = open(save_path, 'w')
        file.write(result)
        file.close()

        self.agents[0].wallet.print_order_log()

    class JSONPack:
        def __init__(self, agents, target):
            from datetime import datetime
            self.timestamp = datetime.now()
            self.fitness_start = Config.start_date
            self.fitness_end = Config.end_date
            self.validation_start = Config.validation_start_date
            self.validation_end = Config.validation_end_date
            self.start_cash = Config.start_cash
            self.target = target
            self.agents = list(map(lambda ag: ag.to_json_ready(), agents))

    def toJSON(self):
        import json
        return json.dumps(self.JSONPack(self.agents[:5], self.target).__dict__, default=str, indent=4)


if __name__ == "__main__":
    read_config()
    worker = GA()
    worker.perform_ga()

    from time import gmtime, strftime

    filename = strftime("%Y-%m-%d %H-%M-%S", gmtime())

    worker.save_results('../' + filename + '.json')
