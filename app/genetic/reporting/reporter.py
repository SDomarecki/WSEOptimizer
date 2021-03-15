import json

from app.config import Config
from app.genetic.genetic_algorithm_worker import GeneticAlgorithmWorker
from app.genetic.genetic_algorithm_worker_json import GeneticAlgorithmWorkerJson


class Reporter:
    def __init__(self, worker: GeneticAlgorithmWorker, config: Config):
        self.worker = worker
        self.config = config

    def save_results(self, save_path: str):
        result_string = self.toJSON()
        self.save_to_file(result_string, save_path)

    def toJSON(self):
        testing_targets = [
            testing_db.benchmark_target for testing_db in self.worker.testing_databases
        ]
        jsonable_self = GeneticAlgorithmWorkerJson(
            self.worker.agents[:5], testing_targets, self.config
        )
        return json.dumps(jsonable_self.__dict__, default=str, indent=2)

    def save_to_file(self, result: str, save_path: str):
        with open(save_path, "w") as file:
            file.write(result)
