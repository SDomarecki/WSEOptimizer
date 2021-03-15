from app.database_scripts.database_preprocessor import DatabasePreprocessor
from app.genetic.main import (
    load_config,
    load_database,
    run_genetic_algorithm,
    save_results,
)


def test_e2e_regular_run_returnsRegularReport():
    path_to_database = "tests/e2e/fast_case/test_database"
    path_to_config = "tests/e2e/fast_case"

    config = load_config(path_to_config)

    dbo = DatabasePreprocessor(path_to_database, config)
    dbo.create_database()

    database_loader = load_database(path_to_database, config)
    worker = run_genetic_algorithm(database_loader, config)
    save_results(worker, config)

    assert True
