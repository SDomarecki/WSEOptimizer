import os
import pathlib

from database_scripts.database_preprocessor import DatabasePreprocessor
from genetic.main import load_config, load_database, run_genetic_algorithm, save_results


def set_pwd_to_application_root():
    wseo_root = pathlib.Path(__file__).parent.parent
    os.chdir(wseo_root)


if __name__ == '__main__':
    set_pwd_to_application_root()

    config = load_config('examples/main/config.json')

    dbo = DatabasePreprocessor(config)
    dbo.create_database()

    database_loader = load_database('database/preprocessed', config)
    worker = run_genetic_algorithm(database_loader, config)
    save_results(worker)
