{
    dataset_name: "perplexity",
    data_dir: "../datasets/perplexity/data",
    evaluation_dir: "../evaluation/perplexity",
    output_dir: "../output/perplexity",
    lexicons_dir: "../datasets/perplexity/lexicons",
    graph_rel_dir: "graphs/subgraphs",
    lexicons: ["hand_populated"],
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