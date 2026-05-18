export COMPOSITION_CONFIG=../configuration_data/pogg_config.json

# activate environment with post-perplexity version of POGG
#export POST_PERPLEXITY_PERPLEXITY_CONFIG=../datasets/perplexity/configs/perplexity_Conrad_2026_config__pre_refactor.json
#export POST_PERPLEXITY_PERPLEXITY_RUN_NAME="post_perplexity__pre_refactor"
#hatch run post-perplexity:perplexity

# activate environment with post-perplexity version of POGG
export POST_PERPLEXITY_PERPLEXITY_CONFIG=../datasets/perplexity/configs/perplexity_Conrad_2026_config.json
export POST_PERPLEXITY_PERPLEXITY_RUN_NAME="post_perplexity__lex_refactor"
hatch run post-perplexity-lex-refactor:perplexity

# run experiment routine on each dataset

# diff against Conrad_2026_results to confirm replication success



# activate environment with post-WebNLG version of POGG

# run experiment routine on each dataset

# diff against Conrad_2026_results to confirm replication success

# diff against post-perplexity to see improvements



# activate environment with post-Logic2Text version of POGG

# run experiment routine on each dataset

# diff against Conrad_2026_results to confirm replication success

# diff against post-WebNLG to see improvements

# diff against post-perplexity to see improvements