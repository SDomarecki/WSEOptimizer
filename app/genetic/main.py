from time import strftime, localtime

from app.genetic.config import Config
from app.genetic.genetic_algorithm_worker import GeneticAlgorithmWorker

if __name__ == '__main__':
    Config()
    worker = GeneticAlgorithmWorker()
    worker.perform_ga()

    filename = strftime('%Y-%m-%d %H-%M-%S', localtime())

    worker.save_results(f'../{filename}.json')
