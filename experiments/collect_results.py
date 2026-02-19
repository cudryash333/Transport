import json
from run_nsga2_experiment import run_nsga2_experiment
from run_dbmosa_experiment import run_dbmosa_experiment


def collect(num_runs=20):
    nsga2_all = []
    dbmosa_all = []

    for seed in range(num_runs):
        nsga2_all.extend(run_nsga2_experiment(seed))
        dbmosa_all.extend(run_dbmosa_experiment(seed))

    with open("results.json_mandl", "w") as f:
        json.dump(
            {
                "nsga2": nsga2_all,
                "dbmosa": dbmosa_all,
            },
            f,
            indent=2,
        )


if __name__ == "__main__":
    collect()
