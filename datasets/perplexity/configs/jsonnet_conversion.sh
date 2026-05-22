CONFIGURATION_DATA_DIR=../../../configuration_data

# generic (for testing during dev)
# pre_refactor
jsonnet --tla-code input='(import "perplexity.jsonnet")' $CONFIGURATION_DATA_DIR/experiment_config_template.jsonnet > "perplexity_config.json"

# Conrad 2026
jsonnet --tla-code input='(import "perplexity_Conrad_2026.jsonnet")' $CONFIGURATION_DATA_DIR/experiment_config_template.jsonnet > "perplexity_Conrad_2026_config.json"
