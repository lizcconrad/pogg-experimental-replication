{
    dataset_name: "perplexity",
    data_dir: "../../datasets/perplexity/data",
    evaluation_dir: "../../Conrad_2026_results/refactor_trace/perplexity",
    output_dir: "../../Conrad_2026_results/refactor_trace/perplexity/post_perplexity__config_refactor/output",
    reports_dir: "../../Conrad_2026_results/refactor_trace/perplexity/post_perplexity__config_refactor/reports",
    lexicons_dir: "./lexicons",
    graph_rel_dir: "graphs/subgraphs",
    lexicons: {
        "hand_populated": {}
    },
    experimental_setups: {
        "config_refactor": {
            "composition_config": "configs/refactor_trace_composition_config.json",
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