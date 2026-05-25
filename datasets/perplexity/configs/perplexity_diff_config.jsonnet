{
    dataset_name: "perplexity",
    diff_dif: "../diffs/perplexity/",
    diff_setups: {
        "hand_populated_vs_random_removals": {
            "baseline_dir": "../output/perplexity/hand_populated",
            "comparison_dir": "../output/perplexity/random_removals"
        }
    },
    split_structure: {
        development: ["HealTheCar", "HealTheTrees", "Tutorial"],
        test: ["AtomicCity", "baby", "HealTheCave", "HealTheFlashback", "HealTheLake", "kidneykwest", "Scenario"]
    },
}