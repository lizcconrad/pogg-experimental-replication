# Runs versions of the pipeline on perplexity data through the stages of the refactor
export COMPOSITION_CONFIG=./configs/refactor_trace_composition_config.json
export RUN_NAME="post_perplexity_" # run name is prepended to experiment name

# run using environment with post-perplexity version of POGG
export EXPERIMENT_CONFIG=./configs/perplexity_Conrad_2026__pre_refactor.json
hatch run post-perplexity:perplexity_refactor_trace

# run using environment with post-perplexity version of POGG after the lexicon refactor
export EXPERIMENT_CONFIG=./configs/perplexity_Conrad_2026__lex_refactor.json
hatch run post-perplexity-lex-refactor:perplexity_refactor_trace

# run using environment with post-perplexity version of POGG after the evaluation refactor
export EXPERIMENT_CONFIG=./configs/perplexity_Conrad_2026__eval_refactor.json
hatch run post-perplexity-eval-refactor:perplexity_refactor_trace

# run using environment with post-perplexity version of POGG after moving semantic composition to another repository
export EXPERIMENT_CONFIG=./configs/perplexity_Conrad_2026__divide_repos.json
hatch run post-perplexity-divide-repos:perplexity_refactor_trace

# run using environment with post-perplexity version of POGG after improving config options
# composition config file is no longer passed in at top level, but each experiment setup specifies it in the experiments JSON file
export EXPERIMENT_CONFIG=./configs/perplexity_Conrad_2026__config_refactor.json
hatch run post-perplexity-config-refactor:perplexity_refactor_trace