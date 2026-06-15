export COMPOSITION_CONFIG=../configuration_data/pogg_config.json

## RUN ALL DATASETS USING post-perplexity VERSION OF POGG ##
export RUN_NAME="post_perplexity_" # run name is prepended to experiment name
# perplexity
export EXPERIMENT_CONFIG=../datasets/perplexity/configs/perplexity_Conrad_2026_config.json
hatch run post-perplexity-config-refactor:run_experiments

# WebNLG
export EXPERIMENT_CONFIG=../datasets/WebNLG/configs/WebNLG_Conrad_2026_config.json
hatch run post-perplexity-config-refactor:run_experiments




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