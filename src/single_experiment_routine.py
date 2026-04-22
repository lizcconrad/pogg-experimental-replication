from pogg.pogg_routine import POGGExperimentConfig

composition_config_path = "../configuration_data/pogg_config.json"
experiment_config_path = "../datasets/perplexity/configs/perplexity_config.json"


experiment_config = POGGExperimentConfig(composition_config_path, experiment_config_path)
experiments = experiment_config.get_all_experiments()
single_experiment = experiments.get_single_experiment("perplexity", "development", "HealTheCar", "hand_populated")
single_experiment.run_experiment()
single_experiment.store_evaluation_report()