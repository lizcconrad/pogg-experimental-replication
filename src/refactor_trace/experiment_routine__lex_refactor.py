from pathlib import Path
import argparse
from pogg.pogg_routine import POGGExperimentsConfig

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--composition_config",  type=str, help="path to the config which specifies grammar information")
parser.add_argument("-e", "--experiment_config",  type=str, help="path to the config which specifies experiments")
parser.add_argument("-r", "--run_name",  type=str, help="path to the config which specifies experiments")

args = parser.parse_args()

composition_config_path = args.composition_config
experiment_config_path = args.experiment_config
run_name = args.run_name


experiments_config = POGGExperimentsConfig(composition_config_path, experiment_config_path, run_name)
# optionally pass in experiment type
experiments = experiments_config.get_all_experiments()

for i, experiment in enumerate(experiments):
    print(f"Running {experiment.full_data_split_name}__{experiment.experiment_name} (experiment {i + 1} of {len(experiments)})...")
    experiment.run_experiment()
    # experiment.store_experiment_output()
    experiment.store_evaluation_report()