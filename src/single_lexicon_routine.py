import sys
import re
import string_processing

from pogg.pogg_routine import POGGExperimentConfig
from pogg.lexicon.auto_lexicon import POGGLexiconAutoFiller
from pogg.lexicon.lexicon_builder import POGGLexiconUtil


composition_config = "../configuration_data/pogg_config.json"
lexicon_templates = "../configuration_data/lexicon_templates/post_perplexity_templates.json"
experiment_config = "../datasets/perplexity/configs/perplexity_config.json"

auto_filling = False
find_new_templates = False
str_processing_fxn = getattr(string_processing, "perplexity")

experiments = POGGExperimentConfig(composition_config, experiment_config)
lexicon_auto_filler = POGGLexiconAutoFiller(composition_config, lexicon_templates)


experiment = experiments.get_experiment("perplexity", "development", "HealTheCar", "hand_populated")
lexicon = experiment.lexicon

if auto_filling:
    lexicon_auto_filler.attempt_auto_filling(lexicon, str_processing_fxn)

lexicon.update_lexicon_files()
ancestors = experiments.get_ancestor_lexicons(lexicon)
POGGLexiconUtil.propagate_lexicon_changes(lexicon, ancestors)

if find_new_templates:
    lexicon_auto_filler.dump_new_templates(lexicon)
