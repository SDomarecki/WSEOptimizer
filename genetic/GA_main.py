import datetime

from genetic.agent import Agent
from genetic.database_loader import read_database
from shared.config import Config
from shared.config import read_config


def ga():
    database = read_database(path_to_database='../res')
    print("Wielkosc bazy danych przed filtrem: " + str(len(database)))
    database = filter_database(database)
    print("Wielkosc bazy danych po filtrze: " + str(len(database)))

    agents = init_agents(Config.initial_population, Config.initial_length)
    generations = Config.iterations
    fitness_number = 1
    for generation in range(generations):

        print('Generation: ' + str(generation))

        for agent in agents:
            if agent.fitness is None:
                print('Fitness check no. ' + str(fitness_number))
                fitness_number += 1
                agent.fitness = fitness(agent, database)
                print(agent.fitness)

        if generation < generations - 1:
            agents = selection(agents)
            agents = crossover(agents)

        agent_mean_fitness = 0
        for i in range(10):
            agent_mean_fitness += agents[i].fitness
        agent_mean_fitness /= 10
        print('Srednia fitnessowa wynosi obecnie ' + str(agent_mean_fitness))

        best_id = 0
        best_score = 0
        for i in range(0, len(agents)):
            if agents[i].fitness is not None and agents[i].fitness > best_score:
                best_score = agents[i].fitness
                best_id = i

        test_agent = Agent(1)
        test_agent.genes = agents[best_id].genes
        test_agent.weights = agents[best_id].weights
        print('Fitness najlepszego agenta')
        print('Dane uczace: ' + str(best_score))
        print('Dane walidacyjne: ' + str(fitness(test_agent, database, validation=True)))
        # order_log = test_agent.wallet.ordersLog
        # for log in order_log:
        #     print(log.to_string())

    ordered_agents = sorted(agents, key=lambda ag: ag.fitness, reverse=True)
    result_string = ''
    for counter, value in enumerate(ordered_agents):
        agent_fitness = value.fitness
        value.reset()
        validated_result = fitness(value, database, validation=True)
        result_string += str(counter + 1) + ") [Val: " + \
                         str(validated_result) + "] [Fit: " + \
                         str(agent_fitness) + "] " + \
                         value.to_string() + "\n"
    save_to_file(result_string)


def filter_database(database):
    # TODO
    min_circulation = Config.min_circulation
    max_circulation = Config.max_circulation

    to_delete = []

    import pandas as pd
    for company in database.values():
        company.technicals = pd.concat([company.technicals.loc[Config.start_date:Config.end_date],
                                        company.technicals.loc[
                                        Config.validation_start_date:Config.validation_end_date]])

        circulation_mean = float(company.technicals['Circulation'].mean())
        if min_circulation != -1 and circulation_mean < Config.min_circulation:
            to_delete.append(company.ticker)
        if max_circulation != -1 and circulation_mean > Config.max_circulation:
            to_delete.append(company.ticker)

    for ticker in to_delete:
        del database[ticker]
    database = filter_by_company_name(database)
    database = filter_by_sector(database)
    return database


def filter_by_company_name(database):
    return database


def filter_by_sector(database):
    sectors = Config.sectors
    to_delete = []

    if sectors[0] == 'All':
        return database

    for company in database.values():
        if company.sector not in sectors:
            to_delete.append(company.ticker)

    for ticker in to_delete:
        del database[ticker]
    return database


def init_agents(population, length):
    return [Agent(length) for _ in range(population)]


# funkcja do obliczenia sprawności agenta
def fitness(tested_agent: Agent, database, validation=False) -> float:
    wallet = tested_agent.wallet

    if not validation:
        start_date = Config.start_date
        end_date = Config.end_date
    else:
        start_date = Config.validation_start_date
        end_date = Config.validation_end_date

    day = start_date
    delta = datetime.timedelta(days=Config.timedelta)
    while day < end_date:
        if day.weekday() == 5:
            day += datetime.timedelta(days=2)
        if day.weekday() == 6:
            day += datetime.timedelta(days=1)

        stock_strengths = {}
        for stock in database.values():
            strength = tested_agent.calculate_strength(stock, day)
            stock_strengths[stock] = strength

        ordered_stocks = []
        ordered_tuples = sorted(stock_strengths.items(), key=lambda kv: kv[1], reverse=True)
        for key, value in ordered_tuples:
            ordered_stocks.append(key)

        wallet.trade(ordered_stocks, day, database)
        day += delta

    if Config.return_method == "total_value":
        return wallet.get_total_value(database, end_date)
    elif Config.return_method == "sharpe":
        return wallet.get_current_sharpe(database)
    else:
        return wallet.get_current_information_ratio()


# fukcja sortująca i niszcząca słabe osobniki
def selection(agents: []):
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    agents = agents[:int(Config.agents_to_drop * len(agents))]
    return agents


# fukcja tworząca nowe osobniki
def crossover(agents: []):
    import random

    offspring = []

    for _ in range(int((Config.initial_population - len(agents)) / 2)):
        parent1 = random.choice(agents)
        parent2 = random.choice(agents)
        child1 = Agent(1)
        child2 = Agent(1)
        split = random.randint(0, Config.initial_length)
        child1.genes = parent1.genes[0:split] + parent2.genes[split:Config.initial_length]
        child2.genes = parent2.genes[0:split] + parent1.genes[split:Config.initial_length]

        child1.weights = parent1.weights[0:split] + parent2.weights[split:Config.initial_length]
        child2.weights = parent2.weights[0:split] + parent1.weights[split:Config.initial_length]

        offspring.append(child1)
        offspring.append(child2)

    offspring = mutation(offspring)
    agents.extend(offspring)

    return agents


# funkcja podmieniająca wagi genów w nowych osobnikach
def mutation(agents: []):
    import random
    for agent in agents:
        for idx, param in enumerate(agent.genes):
            if random.uniform(0.0, 1.0) <= 0.3:
                agent.weights[idx] = random.uniform(0.0, 1.0)
    return agents


def save_to_file(result: str):
    file = open('result.txt', 'w')
    file.write(result)
    file.close()


if __name__ == "__main__":
    read_config()
    ga()
