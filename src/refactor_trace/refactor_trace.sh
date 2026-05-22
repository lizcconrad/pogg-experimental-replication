# Runs versions of the pipeline on perplexity data through the stages of the refactor
export COMPOSITION_CONFIG=../../configuration_data/pogg_config.json

## activate environment with post-perplexity version of POGG
#export POST_PERPLEXITY_PERPLEXITY_CONFIG=./configs/perplexity_Conrad_2026__pre_refactor.json
## run name is prepended to experiment name
#export POST_PERPLEXITY_PERPLEXITY_RUN_NAME="post_perplexity_"
#hatch run post-perplexity:perplexity
#
## activate environment with post-perplexity version of POGG after the lexicon refactor
#export POST_PERPLEXITY_PERPLEXITY_CONFIG=./configs/perplexity_Conrad_2026__lex_refactor.json
## run name is prepended to experiment name
#export POST_PERPLEXITY_PERPLEXITY_RUN_NAME="post_perplexity_"
#hatch run post-perplexity-lex-refactor:perplexity

# activate environment with post-perplexity version of POGG after the evaluation refactor
export POST_PERPLEXITY_PERPLEXITY_CONFIG=./configs/perplexity_Conrad_2026__eval_refactor.json
# run name is prepended to experiment name
export POST_PERPLEXITY_PERPLEXITY_RUN_NAME="post_perplexity_"
hatch run post-perplexity-eval-refactor:perplexity