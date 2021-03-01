from app.config import Config
from app.genetic.agent import Agent
from app.genetic.database_loader import DatabaseLoader
from app.genetic.reporting.plotter import Plotter


class GeneticAlgorithmWorker:
    def __init__(self, loader: DatabaseLoader, config: Config):
        self.next_agent_id = 1
        self.learning_database = loader.learning_database
        self.learning_database_chunks = loader.learning_database_chunks
        self.testing_database = loader.testing_databases
        self.agents = []
        self.config = config
        self.generations = config.iterations
        self.targets = loader.targets
        self.benchmark_learning_wallet = loader.benchmark_learning_wallet
        self.benchmark_testing_wallets = loader.benchmark_testing_wallets
        self.best_scores_learning = []
        self.best_scores_testing = [[]]

        self.selection_operator = None
        self.crossover_operator = None
        self.mutation_operator = None

        self.plotter = Plotter(config)

    def perform_ga(self):
        print(f"Learning database size: {len(self.learning_database)} companies")

        chunks = self.config.chunks

        for generation in range(1, self.generations):
            chunk = generation % chunks
            current_database = self.learning_database_chunks[chunk]

            print(f"Generation: {generation}")

            self.calculate_fitness_on_all_agents(current_database, chunk)
            self.selection()

            if generation < self.generations - 1:
                self.crossover()

            self.calculate_best_agent_validation_performance()
            best_agent = max(self.agents, key=lambda ag: ag.learning_fitness)
            for i in range(len(self.config.validations)):
                self.plotter.print_agent_value_history(
                    best_agent.trader.testing_wallets[i],
                    generation,
                    self.benchmark_testing_wallets[i],
                )
            self.plotter.print_best_agents_learning_performance(
                self.best_scores_learning, self.targets[0]
            )
            self.plotter.print_best_agents_testing_performance(
                self.best_scores_testing, self.targets[:1]
            )

        # Iteration with whole database
        print("Last generation")
        self.calculate_fitness_on_all_agents(self.learning_database, chunks)

        self.agents = sorted(
            self.agents, key=lambda ag: ag.learning_fitness, reverse=True
        )
        best_agent = self.agents[0]
        wallet_to_print = best_agent.trader.training_wallets[self.config.chunks]
        self.plotter.print_agent_value_history(
            wallet_to_print, "last", self.benchmark_learning_wallet
        )
        self.calculate_best_agent_validation_performance()
        for i in range(len(self.config.validations)):
            wallet_to_print = best_agent.trader.testing_wallets[i]
            self.plotter.print_agent_value_history(
                best_agent.trader.testing_wallets[i],
                "last",
                self.benchmark_testing_wallets[i],
            )
        self.plotter.print_best_agents_learning_performance(
            self.best_scores_learning, self.targets[0]
        )
        self.plotter.print_best_agents_testing_performance(
            self.best_scores_testing, self.targets[:1]
        )

        self.calculate_all_validations()

    def calculate_fitness_on_all_agents(self, current_database, chunk):
        for agent in self.agents:
            fit = agent.calculate_learning_fitness(current_database, chunk)
            print(f"[{agent.agent_id}] fitness - {fit}")

    def selection(self):
        self.agents = self.selection_operator.select(self.agents)

    def crossover(self):
        offspring = self.crossover_operator.crossover(self.agents, self.next_agent_id)
        self.next_agent_id += len(offspring)

        mutated_offspring = self.mutation(offspring)
        self.agents.extend(mutated_offspring)

    def mutation(self, agents: [Agent]) -> [Agent]:
        mutated_agents = self.mutation_operator.mutate(agents)
        return mutated_agents

    def calculate_best_agent_validation_performance(self):
        best_agent = max(self.agents, key=lambda ag: ag.learning_fitness)

        for idx, validation in enumerate(self.config.validations):
            fit = best_agent.calculate_testing_fitness(
                self.testing_database[idx],
                idx,
            )
            print(f"[{best_agent.agent_id}] validation #{idx} - {fit}")
            self.append_best_score_on_testing(best_agent, idx)

        print("Best agent performance")
        print(f"Learning: {str(best_agent.learning_fitness)}")
        print("Validations: ")
        for val in best_agent.testing_fitnesses:
            print(str(val))
        print(f"Length of genome: {str(len(best_agent.genes))}")

    def calculate_all_validations(self):
        for agent in self.agents[:5]:
            for val_idx, validation in enumerate(self.config.validations):
                fit = agent.calculate_testing_fitness(
                    self.testing_database[val_idx], val_idx
                )
                print(f"[{agent.agent_id}] validation #{val_idx} - {fit}")

        for val_idx, validation in enumerate(self.config.validations):
            self.append_best_score_on_testing(self.agents[0], val_idx)

    def append_best_score_on_learning(self, agent: Agent):
        if self.config.return_method == "total_value":
            self.best_scores_learning.append(agent.testing_fitnesses[0])
        else:
            self.best_scores_learning.append(
                agent.trader.get_final_testing_fitness(
                    self.learning_database, self.config.chunks
                )
            )

    def append_best_score_on_testing(self, agent: Agent, case):
        if self.config.return_method == "total_value":
            self.best_scores_testing[case].append(agent.testing_fitnesses[0])
        else:
            self.best_scores_testing[case].append(
                agent.trader.get_final_testing_fitness(
                    self.testing_database[case], case
                )
            )
