CONFIGURATION_DATA_DIR=../../../configuration_data

# generic (for testing during dev)
jsonnet --tla-code input='(import "perplexity.jsonnet")' $CONFIGURATION_DATA_DIR/experiment_config_template.jsonnet > "perplexity_config.json"

# Conrad 2026
jsonnet --tla-code input='(import "perplexity_Conrad_2026.jsonnet")' $CONFIGURATION_DATA_DIR/experiment_config_template.jsonnet > "perplexity_Conrad_2026_config.json"


# diffs
jsonnet --tla-code input='(import "perplexity_diff_config.jsonnet")' $CONFIGURATION_DATA_DIR/diff_template.jsonnet > "perplexity_diff_config.json"
