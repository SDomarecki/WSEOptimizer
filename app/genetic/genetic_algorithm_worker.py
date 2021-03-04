from app.config import Config
from app.genetic.agent import Agent


class GeneticAlgorithmWorker:
    def __init__(self, config: Config):
        self.config = config

        self.next_agent_id = 1
        self.learning_database = None
        self.testing_databases = None
        self.chunk_size = 0

        self.agents = []
        self.benchmark_agent = None
        self.offspring = []
        self.generations = config.iterations

        self.best_scores_learning = []
        self.best_scores_testing = [[]]

        self.selection_operator = None
        self.crossover_operator = None
        self.mutation_operator = None

        self.plotter = None

    def perform_ga(self):
        print(
            f"Learning database size: {len(self.learning_database.companies)} companies"
        )
        self.benchmark_agent.calculate_benchmarks(
            self.learning_database, self.testing_databases
        )

        for generation in range(1, self.generations):
            self.normal_generation(generation)
        self.last_generation()

    def normal_generation(self, generation):
        print(f"Generation: {generation}")

        chunk = generation % self.config.chunks
        chunk_start = chunk * self.chunk_size
        chunk_end = (chunk + 1) * self.chunk_size
        current_database = self.learning_database.companies[chunk_start:chunk_end]

        self.calculate_fitness_on_all_agents(current_database, chunk)
        self.sort_agents()
        self.use_genetic_operators()

        best_agent = self.agents[0]

        self.calculate_agent_validation_performance(best_agent)
        self.compare_testing_agent_value_history_to_benchmark(best_agent, generation)
        self.print_best_agents_performance()

        print("Best agent performance")
        print(f"Learning: {str(best_agent.learning_fitness)}")
        print("Validations: ")
        for val in best_agent.testing_fitnesses:
            print(str(val))

    def last_generation(self):
        # Iteration with whole database
        print("Last generation")
        self.calculate_fitness_on_all_agents(
            self.learning_database.companies, self.config.chunks
        )
        self.sort_agents()

        best_agent = self.agents[0]

        self.compare_learning_agent_value_history_to_benchmark(best_agent)
        self.calculate_agent_validation_performance(best_agent)
        self.append_best_agent_scores_on_testing()
        self.compare_testing_agent_value_history_to_benchmark(best_agent, "last")
        self.print_best_agents_performance()

        self.calculate_all_validations()

    def calculate_fitness_on_all_agents(self, current_database, chunk):
        for agent in self.agents:
            fit = agent.calculate_learning_fitness(current_database, chunk)
            print(f"[{agent.agent_id}] fitness - {fit}")

    def sort_agents(self):
        self.agents = sorted(
            self.agents, key=lambda ag: ag.learning_fitness, reverse=True
        )

    def use_genetic_operators(self):
        self.selection()
        self.crossover()
        self.mutation()

    def selection(self):
        self.agents = self.selection_operator.select(self.agents)

    def crossover(self):
        self.offspring = self.crossover_operator.crossover(
            self.agents, self.next_agent_id
        )
        self.next_agent_id += len(self.offspring)

    def mutation(self):
        mutated_agents = self.mutation_operator.mutate(self.offspring)
        self.agents.extend(mutated_agents)

    def calculate_agent_validation_performance(self, agent: Agent):
        for idx in range(len(self.config.validations)):
            fit = agent.calculate_testing_fitness(
                self.testing_databases[idx].companies, idx
            )
            print(f"[{agent.agent_id}] validation #{idx} - {fit}")

    def calculate_all_validations(self):
        for agent in self.agents[:5]:
            self.calculate_agent_validation_performance(agent)
        self.append_best_agent_scores_on_testing()

    def append_best_agent_score_on_learning(self):
        best_agent = self.agents[0]
        if self.config.return_method == "total_value":
            self.best_scores_learning.append(best_agent.learning_fitness[0])
        else:
            self.best_scores_learning.append(
                best_agent.trader.get_final_testing_fitness(
                    self.learning_database, self.config.chunks
                )
            )

    def append_best_agent_scores_on_testing(self):
        best_agent = self.agents[0]
        for idx in range(len(self.config.validations)):
            if self.config.return_method == "total_value":
                self.best_scores_testing[idx].append(best_agent.testing_fitnesses[0])
            else:
                self.best_scores_testing[idx].append(
                    best_agent.trader.get_final_testing_fitness(
                        self.testing_databases[idx], idx
                    )
                )

    def print_best_agents_performance(self):
        self.plotter.print_best_agents_learning_performance(
            self.best_scores_learning, self.learning_database.benchmark_target
        )
        self.plotter.print_best_agents_testing_performance(
            self.best_scores_testing,
            [db.benchmark_target for db in self.testing_databases],
        )

    def compare_testing_agent_value_history_to_benchmark(self, agent, generation):
        for i in range(len(self.config.validations)):
            wallet_to_print = agent.trader.testing_wallets[i]
            self.plotter.print_agent_value_history(
                wallet_to_print, generation, self.testing_databases[i].benchmark_wallet
            )

    def compare_learning_agent_value_history_to_benchmark(self, agent):
        wallet_to_print = agent.trader.training_wallets[self.config.chunks]
        self.plotter.print_agent_value_history(
            wallet_to_print, "last", self.learning_database.benchmark_wallet
        )
