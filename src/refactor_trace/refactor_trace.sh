# Runs versions of the pipeline on perplexity data through the stages of the refactor
export COMPOSITION_CONFIG=./configs/refactor_trace_composition_config.json

# run using environment with post-perplexity version of POGG
export POST_PERPLEXITY_PERPLEXITY_CONFIG=./configs/perplexity_Conrad_2026__pre_refactor.json
# run name is prepended to experiment name
export POST_PERPLEXITY_PERPLEXITY_RUN_NAME="post_perplexity_"
hatch run post-perplexity:perplexity_refactor_trace

# run using environment with post-perplexity version of POGG after the lexicon refactor
export POST_PERPLEXITY_PERPLEXITY_CONFIG=./configs/perplexity_Conrad_2026__lex_refactor.json
# run name is prepended to experiment name
export POST_PERPLEXITY_PERPLEXITY_RUN_NAME="post_perplexity_"
hatch run post-perplexity-lex-refactor:perplexity_refactor_trace

# run using environment with post-perplexity version of POGG after the evaluation refactor
export POST_PERPLEXITY_PERPLEXITY_CONFIG=./configs/perplexity_Conrad_2026__eval_refactor.json
# run name is prepended to experiment name
export POST_PERPLEXITY_PERPLEXITY_RUN_NAME="post_perplexity_"
hatch run post-perplexity-eval-refactor:perplexity_refactor_trace

# run using environment with post-perplexity version of POGG after moving semantic composition to another repository
export POST_PERPLEXITY_PERPLEXITY_CONFIG=./configs/perplexity_Conrad_2026__divide_repos.json
# run name is prepended to experiment name
export POST_PERPLEXITY_PERPLEXITY_RUN_NAME="post_perplexity_"
hatch run post-perplexity-divide-repos:perplexity_refactor_trace

# run using environment with post-perplexity version of POGG after improving config options
# composition config file is no longer passed in at top level, but each experiment setup specifies it in the experiments JSON file
export POST_PERPLEXITY_PERPLEXITY_CONFIG=./configs/perplexity_Conrad_2026__config_refactor.json
# run name is prepended to experiment name
export POST_PERPLEXITY_PERPLEXITY_RUN_NAME="post_perplexity_"
hatch run post-perplexity-config-refactor:perplexity_refactor_trace