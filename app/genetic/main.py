import json
from time import strftime, localtime

from app.config import Config
from app.genetic.database_loader import DatabaseLoader
from app.genetic.genetic_algorithm_worker import GeneticAlgorithmWorker
from app.genetic.genetic_algorithm_worker_builder import GeneticAlgorithmWorkerBuilder


def load_config(path: str) -> Config:
    with open(path) as f:
        dict_config = json.load(f)

    config = Config()
    config.fetch_from_dict(dict_config)
    return config


def load_database(path: str, config: Config) -> DatabaseLoader:
    return DatabaseLoader(path, config)


def run_genetic_algorithm(database_loader: DatabaseLoader, config: Config) -> GeneticAlgorithmWorker:
    worker = GeneticAlgorithmWorkerBuilder().build(database_loader, config)
    worker.perform_ga()
    return worker


def save_results(worker: GeneticAlgorithmWorker):
    filename = strftime('%Y-%m-%d %H-%M-%S', localtime())
    worker.save_results(f'../{filename}.json')
