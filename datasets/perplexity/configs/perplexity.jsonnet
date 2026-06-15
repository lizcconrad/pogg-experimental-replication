{
    dataset_name: "perplexity",
    data_dir: "../datasets/perplexity/data",
    evaluation_dir: "../evaluation/perplexity",
    output_dir: "../output/perplexity",
    reports_dir: "../reports/perplexity",
    lexicons_dir: "../datasets/perplexity/lexicons",
    graph_rel_dir: "graphs/subgraphs",
    lexicons: {
        "hand_populated": {},
        "random_removals": {}
    },
    experimental_setups: {
        "hand_populated": {
            "composition_config": "../ERG_versions/ERG_2023_GP2/ERG_2023_GP2_config.json",
            "lexicon_name": "hand_populated",
            "SEMENT_processing": [],
            "result_processing": []
        },
        "random_removals": {
            "composition_config": "../ERG_versions/ERG_2023_GP2/ERG_2023_GP2_config.json",
            "lexicon_name": "random_removals",
            "SEMENT_processing": [],
            "result_processing": []
        }
    },
    split_structure: {
        development: ["HealTheCar", "HealTheTrees", "Tutorial"],
        test: ["AtomicCity", "baby", "HealTheCave", "HealTheFlashback", "HealTheLake", "kidneykwest", "Scenario"]
    },
}