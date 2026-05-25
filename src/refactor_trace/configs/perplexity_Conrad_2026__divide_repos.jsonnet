{
    dataset_name: "perplexity",
    data_dir: "../../datasets/perplexity/data",
    evaluation_dir: "../../Conrad_2026_results/refactor_trace/perplexity",
    output_dir: "../../Conrad_2026_results/refactor_trace/perplexity/post_perplexity__divide_repos/output",
    reports_dir: "../../Conrad_2026_results/refactor_trace/perplexity/post_perplexity__divide_repos/reports",
    lexicons_dir: "../../datasets/perplexity/lexicons",
    graph_rel_dir: "graphs/subgraphs",
    lexicons: ["hand_populated"],
    experimental_setups: {
        "divide_repos": {
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