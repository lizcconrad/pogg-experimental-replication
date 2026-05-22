CONFIGURATION_DATA_DIR=../../../configuration_data

# Conrad_2026
# pre_refactor
jsonnet --tla-code input='(import "perplexity_Conrad_2026__pre_refactor.jsonnet")' $CONFIGURATION_DATA_DIR/experiment_config_template__pre_refactor.jsonnet > "perplexity_Conrad_2026__pre_refactor.json"

# lex_refactor
jsonnet --tla-code input='(import "perplexity_Conrad_2026__lex_refactor.jsonnet")' $CONFIGURATION_DATA_DIR/experiment_config_template.jsonnet > "perplexity_Conrad_2026__lex_refactor.json"

# eval_refactor
jsonnet --tla-code input='(import "perplexity_Conrad_2026__eval_refactor.jsonnet")' $CONFIGURATION_DATA_DIR/experiment_config_template.jsonnet > "perplexity_Conrad_2026__eval_refactor.json"

