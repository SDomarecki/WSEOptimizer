import json
import random
from time import strftime, localtime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from app.genetic.agent import Agent
from app.genetic.config import Config
from app.genetic.database_loader import DatabaseLoader
from genetic.crossover.constant_crossover_operator import ConstantCrossoverOperator
from genetic.crossover.non_constant_crossover_operator import NonConstantCrossoverOperator
from genetic.mutation.normalization_mutation_operator import NormalizationMutationOperator
from genetic.selection.rating_selection import RatingSelectionOperator
from genetic.selection.roulette_selection import RouletteSelectionOperator
from genetic.selection.tournament_selection import TournamentSelectionOperator


class GeneticAlgorithmWorker:

    def __init__(self):
        loader = DatabaseLoader('database/preprocessed', Config.benchmark)

        self.next_agent_id = 1
        self.learning_database = loader.learning_database
        self.learning_database_chunks = loader.learning_database_chunks
        self.testing_database = loader.testing_databases
        self.agents = []
        self.generations = Config.iterations
        self.targets = loader.targets
        self.benchmark_learning_wallet = loader.benchmark_learning_wallet
        self.benchmark_testing_wallets = loader.benchmark_testing_wallets
        self.best_scores_learning = []
        self.best_scores_testing = [[]]

        self.init_agents()
        self.init_selection_operator()
        self.init_crossover_operator()
        self.init_mutation_operator()

    def init_agents(self):
        if Config.constant_length:
            self.init_constant_length_agents()
        else:
            self.init_non_constant_length_agents()
        self.next_agent_id += Config.initial_population

    def init_constant_length_agents(self):
        self.agents = [Agent(self.next_agent_id + i, Config.initial_length, len(Config.validations))
                       for i in
                       range(Config.initial_population)]

    def init_non_constant_length_agents(self):
        self.agents = [Agent(self.next_agent_id + i, random.randint(2, Config.max_genes), len(Config.validations))
                       for i in
                       range(Config.initial_population)]

    def init_selection_operator(self):
        method = Config.selection_method
        if method == 'rating':
            self.selection_operator = RatingSelectionOperator(Config.agents_to_save)
        elif method == 'tournament':
            self.selection_operator = TournamentSelectionOperator(Config.agents_to_save)
        elif method == 'roulette':
            self.selection_operator = RouletteSelectionOperator(Config.agents_to_save)
        else:
            raise NotImplementedError('Wrong selection method')

    def init_crossover_operator(self):
        to_create = int((Config.initial_population - Config.agents_to_save) / 2)
        if Config.constant_length:
            self.crossover_operator = ConstantCrossoverOperator(Config.initial_length, to_create, Config.validations)
        else:
            self.crossover_operator = NonConstantCrossoverOperator(Config.max_genes, to_create, Config.validations)

    def init_mutation_operator(self):
        self.mutation_operator = NormalizationMutationOperator(Config.mutation_rate)

    def perform_ga(self):
        print(f'Learning database size: {len(self.learning_database)} companies')

        chunks = Config.chunks

        for generation in range(1, self.generations):
            current_database = self.learning_database_chunks[generation % chunks]

            print(f'Generation: {generation}')

            for agent in self.agents:
                fit = agent.calculate_fitness(current_database, Config.start_date, Config.end_date)
                print(f'[{agent.id}] fitness - {fit}')
            self.selection()

            if generation < self.generations - 1:
                self.crossover()

            # self.print_agent_value_history(generation)
            self.calculate_best_agent_validation_performance()
            for idx, _ in enumerate(Config.validations):
                self.print_agent_value_history(generation, idx)
            self.print_best_agents_performance()

        # Iteration with whole database
        print('Last generation')
        for agent in self.agents:
            fit = agent.calculate_fitness(self.learning_database, Config.start_date, Config.end_date)
            print(f'[{agent.id}] fitness - {fit}')
        self.agents = sorted(self.agents, key=lambda ag: ag.fitness, reverse=True)

        self.print_agent_value_history('last')
        self.calculate_best_agent_validation_performance()
        for idx, _ in enumerate(Config.validations):
            self.print_agent_value_history('last', idx)
        self.print_best_agents_performance()

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
        best_agent = max(self.agents, key=lambda ag: ag.fitness)
        if Config.return_method == 'total_value':
            self.best_scores_learning.append(best_agent.fitness)
        else:
            self.best_scores_learning.append(
                best_agent.wallet.get_total_value(self.learning_database, Config.end_date))

        for idx, validation in enumerate(Config.validations):
            fit = best_agent.calculate_fitness(self.testing_database[idx], validation[0], validation[1],
                                               validation_case=idx)
            print(f'[{best_agent.id}] validation #{idx} - {fit}')
            if Config.return_method == 'total_value':
                self.best_scores_testing[idx].append(best_agent.validations[0])
            else:
                self.best_scores_testing[idx].append(
                    best_agent.wallet.get_total_value(self.testing_database[idx], validation[1]))

        print('Best agent performance')
        print(f'Learning: {str(best_agent.fitness)}')
        print('Validations: ')
        for val in best_agent.validations:
            print(str(val))
        print(f'Length of genome: {str(len(best_agent.genes))}')

    def print_agent_value_history(self, generation, benchmark_wallet_index=-1):
        best_agent = max(self.agents, key=lambda ag: ag.fitness)
        if benchmark_wallet_index == -1:
            benchmark_wallet = self.benchmark_learning_wallet
        else:
            benchmark_wallet = self.benchmark_testing_wallets[benchmark_wallet_index]

        x = mdates.date2num(best_agent.wallet.valueTimestamps)
        y = best_agent.wallet.valueHistory
        plt.xticks(rotation=45)
        plt.gcf().subplots_adjust(bottom=0.15)
        plt.plot_date(x, benchmark_wallet,
                      color='#d62f2f',
                      linestyle='solid',
                      marker="",
                      label='Target')
        plt.plot_date(x, y, '-g',
                      label='Total value')
        plt.legend(loc='upper left')
        plt.savefig(f'../{str(generation)}_{str(benchmark_wallet_index)}.png', dpi=500)
        plt.close()

    def print_best_agents_performance(self):

        plt.plot(self.best_scores_learning,
                 label='Best agent end value')
        plt.axhline(self.targets[0],
                    color='r',
                    linestyle='--',
                    label='Target end value')
        plt.legend(loc='upper left')
        plt.savefig('../elite_perf_learning.png', dpi=500)
        plt.close()

        targets = self.targets[1:]
        for idx, _ in enumerate(Config.validations):
            plt.plot(self.best_scores_testing[idx],
                     label='Best agent end value')
            plt.axhline(targets[idx],
                        color='r',
                        linestyle='--',
                        label='Target end value')
            plt.legend(loc='upper left')
            plt.savefig(f'../elite_perf_test_{str(idx)}.png', dpi=500)
            plt.close()

    def save_results(self, save_path: str):
        self.calculate_all_validations()
        self.print_best_agents_performance()
        result_string = self.toJSON()
        self.save_to_file(result_string, save_path)

    def calculate_all_validations(self):
        for _, agent in enumerate(self.agents[:5]):
            for val_idx, validation in enumerate(Config.validations):
                fit = agent.calculate_fitness(self.testing_database[val_idx], validation[0], validation[1],
                                              validation_case=val_idx)
                print(f'[{agent.id}] validation #{val_idx} - {fit}')

        for val_idx, validation in enumerate(Config.validations):
            if Config.return_method == 'total_value':
                self.best_scores_testing[val_idx].append(self.agents[0].validations[val_idx])
            else:
                self.best_scores_testing[val_idx].append(
                    self.agents[0].wallet.get_total_value(self.testing_database[val_idx],
                                                          Config.validations[val_idx][1]))

    def save_to_file(self, result: str, save_path: str):
        file = open(save_path, 'w')
        file.write(result)
        file.close()

    class JSONPack:
        def __init__(self, agents, targets):
            self.timestamp = strftime('%Y-%m-%d %H-%M-%S', localtime())
            self.fitness_start = Config.start_date
            self.fitness_end = Config.end_date

            self.validations = []
            for idx, target in enumerate(targets):
                self.validations.append({
                    'start_date': Config.validations[idx][0],
                    'end_date': Config.validations[idx][1],
                    'target': target
                })
            self.start_cash = Config.start_cash
            self.agents = list(map(lambda ag: ag.to_json_ready(), agents))

    def toJSON(self):
        return json.dumps(self.JSONPack(self.agents[:5], self.targets[1:]).__dict__, default=str, indent=2)
