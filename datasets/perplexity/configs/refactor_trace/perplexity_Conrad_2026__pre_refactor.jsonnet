{
    dataset_name: "perplexity",
    data_dir: "../datasets/perplexity/data",
    evaluation_dir: "../Conrad_2026_results/refactor_trace/perplexity",
    lexicons_dir: "../datasets/perplexity/lexicons",
    graph_rel_dir: "graphs/subgraphs",
    experimental_setups: {
        "pre_lex_refactor": {
            "lexicon_name": "hand_populated_old_format",
            "SEMENT_processing": [],
            "result_processing": []
        }
    },
    split_structure: {
        development: ["HealTheCar", "HealTheTrees", "Tutorial"],
        test: ["AtomicCity", "baby", "HealTheCave", "HealTheFlashback", "HealTheLake", "kidneykwest", "Scenario"]
    },
}