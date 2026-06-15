# routine to aid in expanding/completing the lexicon before the POGG routine is run on the finished lexicon
import os
import json
import re
from itertools import permutations
from pathlib import Path
from delphin import ace
from pogg.lexicon.lexicon_builder import POGGLexiconUtil
from pogg.lexicon.auto_lexicon import POGGLexiconAutoFiller
from pogg.my_delphin import sementcodecs
from pogg.pogg_config import POGGConfig
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra
from pogg.semantic_composition.semantic_composition import SemanticComposition
from pogg.graph_to_SEMENT.graph_to_SEMENT import POGGGraphConverter
from pogg.semantic_composition.sement_util import POGGSEMENTUtil



# instantiate POGG objects
pogg_config = POGGConfig("../../pogg_configs/config.yml")
sem_alg = SemanticAlgebra(pogg_config)
sem_comp = SemanticComposition(sem_alg)

converter = POGGGraphConverter(sem_comp)

auto_filler = POGGLexiconAutoFiller(pogg_config, "../../template_lexical_entries.json")

categories = [
    "Airport",
    "Artist",
    "Astronaut",
    "Athlete",
    "Building",
    "CelestialBody",
    "City",
    "ComicsCharacter",
    "Company",
    "Food",
    "MeanOfTransportation",
    "Monument",
    "Politician",
    "SportsTeam",
    "University",
    "WrittenWork"
]
triple_amounts = ["1triples", "2triples", "3triples"]


auto_filling = False
category = "WrittenWork"
triple_amount = "1triples"

if triple_amount == "1triples":
    data_segment_dir = f"{category}_allSolutions"
else:
    data_segment_dir = f"{category}"


lexicon_dir = Path(f"../pogg_formatted/dev/{triple_amount}/{data_segment_dir}/lexicon")
lexicon_dir.mkdir(parents=True, exist_ok=True)
data_path = Path(f"../pogg_formatted/dev/{triple_amount}/{data_segment_dir}/graphs/modified_triplesets/json/")

# load data from graph json
graph_json_path = Path(data_path, f"{category}_full_graph_format.json")
with open(graph_json_path, "r") as f:
    full_graph_json = json.load(f)


# create skeleton from all data
lexicon_skeleton = POGGLexiconUtil.create_lexicon_skeleton(full_graph_json)

# Initialize directory (POGGLexiconUtil.initialize_directory will not overwrite files if they exist)
POGGLexiconUtil.initialize_lexicon_directory(category, lexicon_dir, lexicon_skeleton)


# attempt to automatically fill in node entries
if auto_filling:
    with open(Path(lexicon_dir, f"{category}_lexicon_incomplete_entries.json"), "r") as incomplete_f:
        incomplete_json = json.load(incomplete_f)

        for node_key in incomplete_json['node_keys']:

            # check for auto notes
            # if you want to skip parsing certain nodes, add auto notes and this will skip it
            if "auto" in incomplete_json['node_keys'][node_key]:
                continue

            string_to_parse = re.sub(",*_", " ", node_key)
            print(string_to_parse)

            completed_lexical_entry = auto_filler.find_and_fill_template(string_to_parse)
            if completed_lexical_entry is not None:
                print(f"AUTO FILLING {node_key}...")
                incomplete_json['node_keys'][node_key] = completed_lexical_entry

    with open(Path(lexicon_dir, f"{category}_lexicon_incomplete_entries.json"), "w") as incomplete_f:
        # dump incomplete back into file
        json.dump(incomplete_json, incomplete_f, indent=4)


# expand any entries that have been filled in by user or auto-filler
POGGLexiconUtil.update_lexicon_files(lexicon_dir, None)

# go through complete lexicon and add new templates to template file
with open(Path(lexicon_dir, f"{category}_lexicon_complete_entries.json"), "r") as complete_f:
    complete_json = json.load(complete_f)
    auto_filler.dump_new_templates(complete_json)













