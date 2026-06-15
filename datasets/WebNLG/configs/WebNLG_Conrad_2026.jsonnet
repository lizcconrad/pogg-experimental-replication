{
    dataset_name: "WebNLG",
    data_dir: "../datasets/WebNLG/pogg_formatted_data",
    evaluation_dir: "../Conrad_2026_results/evaluation/WebNLG",
    output_dir: "../Conrad_2026_results/output/WebNLG",
    reports_dir: "../Conrad_2026_results/reports/WebNLG",
    lexicons_dir: "../datasets/WebNLG/lexicons",
    graph_rel_dir: "graphs/modified_triplesets",
    lexicons: {
        "post_perplexity_no_numbers": {
            "lexicon_dir": "../datasets/WebNLG/lexicons/post_perplexity_no_numbers",
            "auto_filler_settings": {
                "auto_fill": true,
                "auto_approve": false,
                "auto_create_templates": false,
                "template_files": [
                    "../configuration_data/lexicon_templates/perplexity/perplexity_templates.json",
                    "../configuration_data/lexicon_templates/webnlg/webnlg_post_perplexity_templates.json"
                ],
                "blocked_templates": [
                    "TEMPLATE_1"
                ],
                "template_dump_file": "../configuration_data/lexicon_templates/webnlg/webnlg_post_perplexity_templates.json"
            }
        }
    },
    experimental_setups: {
        "post_perplexity_no_numbers": {
            "composition_config": "../ERG_versions/ERG_2023_GP2/ERG_2023_GP2_config.json",
            "lexicon_name": "post_perplexity_no_numbers",
            "SEMENT_processing": [],
            "result_processing": []
        }
    },
    categories: [
        "Airport",
        "Artist",
        "Astronaut",
        "Athlete",
        "Building",
        "CelestialBody",
        "City",
        "ComicsCharacter",
        "Company",
        "Food",
        "MeanOfTransportation",
        "Monument",
        "Politician",
        "SportsTeam",
        "University",
        "WrittenWork"
    ],
    split_structure: {
        dev: {
            "1triples": [x for x in $.categories],
            "2triples": [x for x in $.categories],
            "3triples": [x for x in $.categories]
        }
    }
}
