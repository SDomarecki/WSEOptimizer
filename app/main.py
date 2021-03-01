import os
import pathlib

from app.database_scripts.database_preprocessor import DatabasePreprocessor
from app.genetic.main import (
    load_config,
    load_database,
    run_genetic_algorithm,
    save_results,
)


def set_pwd_to_application_root():
    wseo_root = pathlib.Path(__file__).parent.parent
    os.chdir(wseo_root)


if __name__ == "__main__":
    set_pwd_to_application_root()

    path_to_database = "database/preprocessed"
    path_to_config = "examples/main/config.json"

    config = load_config(path_to_config)

    dbo = DatabasePreprocessor(path_to_database, config)
    dbo.create_database()

    database_loader = load_database(path_to_database, config)
    worker = run_genetic_algorithm(database_loader, config)
    save_results(worker, config)
