import json
from time import strftime, localtime

from app.config import Config
from app.genetic.database_loader import DatabaseLoader
from app.genetic.genetic_algorithm_worker import GeneticAlgorithmWorker
from app.genetic.genetic_algorithm_worker_builder import GeneticAlgorithmWorkerBuilder
from app.genetic.reporting.reporter import Reporter


def load_config(path: str) -> Config:
    with open(f"{path}/config.json") as f:
        dict_config = json.load(f)

    config = Config()
    config.fetch_from_dict(dict_config)
    config.path_to_config = path
    return config


def load_database(path: str, config: Config) -> DatabaseLoader:
    return DatabaseLoader(path, config)


def run_genetic_algorithm(
    database_loader: DatabaseLoader, config: Config
) -> GeneticAlgorithmWorker:
    worker = GeneticAlgorithmWorkerBuilder().build(database_loader, config)
    worker.perform_ga()
    return worker


def save_results(worker: GeneticAlgorithmWorker, config: Config):
    filename = strftime("%Y-%m-%d %H-%M-%S", localtime())
    reporter = Reporter(worker, config)
    reporter.save_results(f"{config.path_to_config}/{filename}.json")
