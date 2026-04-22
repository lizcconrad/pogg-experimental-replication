{
    dataset_name: "perplexity",
    data_dir: "../datasets/perplexity/data",
    evaluation_dir: "../Conrad_2026_results/evaluation/perplexity",
    lexicons_dir: "../datasets/perplexity/lexicons",
    graph_rel_dir: "graphs/subgraphs",
    experimental_setups: {
        "hand_populated": {
            "lexicon_name": "hand_populated",
            "SEMENT_processing": [],
            "result_processing": []
        }
    },
    split_structure: {
        development: ["HealTheCar", "HealTheTrees", "Tutorial"],
        test: ["AtomicCity", "baby", "HealTheCave", "HealTheFlashback", "HealTheLake", "kidneykwest", "Scenario"]
    },
}