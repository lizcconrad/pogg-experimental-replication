import os
import json
import string_processing

from pogg.lexicon import POGGLexicon, POGGLexiconAutoFiller
from pogg.data_handling import POGGDataset

composition_config = "../configuration_data/pogg_config.json"
experiment_config = "../datasets/WebNLG/configs/WebNLG_config.json"
lexicon_templates = ["../configuration_data/lexicon_templates/perplexity_templates.json"]
template_dump_file = "../configuration_data/lexicon_templates/webnlg_templates.json"


auto_approve = True
auto_create_templates = False
str_processing_fxn = getattr(string_processing, "webnlg")

with open(experiment_config, "r") as f:
    config_json = json.load(f)

dataset = POGGDataset(config_json)
auto_filler = POGGLexiconAutoFiller(composition_config, lexicon_templates,
                                    auto_approve=auto_approve, string_processing_fxn=None,
                                    auto_create_templates=auto_create_templates, dump_file=template_dump_file)

lexicon = POGGLexicon("demo", config_json["lexicon_dir"] + "/auto_approve", dataset, auto_filler=auto_filler)

data_split = dataset.get_data_split("demo", "dev", "1triples", "Airport_allSolutions")
lexicon.set_workspace_split(data_split)
lexicon.update_lexicon_files()

auto_filler.dump_new_templates(lexicon.node_entries)

