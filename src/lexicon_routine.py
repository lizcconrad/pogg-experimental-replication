import os
import json
import string_processing

from pogg.lexicon import POGGLexicon, POGGLexiconAutoFiller
from pogg.data_handling import POGGDataset

# each experiment has a composition config, but each lexicon does not, so when working on a lexicon I just have to pick one
composition_config = "../ERG_versions/ERG_2023_GP2/ERG_2023_GP2_config.json"
experiment_config = "../datasets/WebNLG/configs/WebNLG_config.json"
str_processing_fxn = getattr(string_processing, "webnlg")

# name of lexicon being worked on
lexicon_name = "post_perplexity"

with open(experiment_config, "r") as f:
    config_json = json.load(f)

dataset = POGGDataset(config_json)

lexicon_info = config_json["lexicons"][lexicon_name]
auto_filler_settings = lexicon_info["auto_filler_settings"]

if auto_filler_settings["auto_fill"]:
    auto_filler = POGGLexiconAutoFiller(composition_config, auto_filler_settings["template_files"],
                                        auto_approve=auto_filler_settings["auto_approve"],
                                        global_blocked_templates=auto_filler_settings["blocked_templates"],
                                        string_processing_fxn=str_processing_fxn,
                                        auto_create_templates=auto_filler_settings["auto_create_templates"],
                                        dump_file=auto_filler_settings["template_dump_file"])
else:
    auto_filler = None

lexicon = POGGLexicon(config_json["lexicons"][lexicon_name]["lexicon_dir"], dataset,
                      imported_lexicon_paths=lexicon_info["imported_lexicon_paths"], auto_filler=auto_filler)

# remove splits already worked through
# one_triples = dataset.get_data_split("WebNLG", "dev", "1triples")
removal_splits = []


data_split = dataset.get_data_split("WebNLG", "dev")
lexicon.set_workspace_split(data_split, removal_splits)
lexicon.update_lexicon_files()


auto_filler.dump_new_templates(lexicon.node_entries)

