{
    dataset_name: "perplexity",
    data_dir: "../../datasets/perplexity/data",
    evaluation_dir: "../../Conrad_2026_results/refactor_trace/perplexity",
    output_dir: "../../Conrad_2026_results/refactor_trace/perplexity/post_perplexity__eval_refactor/output",
    reports_dir: "../../Conrad_2026_results/refactor_trace/perplexity/post_perplexity__eval_refactor/reports",
    lexicons_dir: "../../datasets/perplexity/lexicons",
    graph_rel_dir: "graphs/subgraphs",
    lexicons: ["hand_populated"],
    experimental_setups: {
        "eval_refactor": {
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