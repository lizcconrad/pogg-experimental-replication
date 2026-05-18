import os
import json

from pogg.lexicon import POGGLexicon
from pogg.data_handling import POGGDataset

os.chdir("../../../src/")

experiment_config = "../datasets/perplexity/configs/perplexity_config.json"

lexicon_name = "hand_populated"


with open(experiment_config, "r") as f:
    config_json = json.load(f)

dataset = POGGDataset(config_json)
lexicon = POGGLexicon(config_json["dataset_name"], config_json["lexicons"][lexicon_name]["lexicon_dir"], dataset)
lexicon.update_lexicon_files()

old_complete = "../datasets/perplexity/lexicons/hand_populated_old_format/hand_populated_lexicon_complete_entries.json"
with open(old_complete, "r") as f:
    old_complete_json = json.load(f)

for node_key, node_entry in old_complete_json["node_keys"].items():
    if node_key in lexicon.workspace_node_entries:
        lexicon.workspace_node_entries[node_key].entry_in_dict_format = node_entry
        lexicon.workspace_node_entries[node_key].approved = True

for edge_key, edge_entry in old_complete_json["edge_keys"].items():
    if edge_key in lexicon.workspace_edge_entries:
        lexicon.workspace_edge_entries[edge_key].entry_in_dict_format = edge_entry
        lexicon.workspace_edge_entries[edge_key].approved = True


lexicon.update_lexicon_files()

