# routine to aid in expanding/completing the lexicon before the POGG routine is run on the finished lexicon
import os
import json
from pathlib import Path
from pogg.lexicon.lexicon_builder import POGGLexiconUtil

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

lexicon_name = "webnlg_dev"
lexicon_dir = Path("../pogg_formatted_data_stash/dev/1triples/lexicon")
lexicon_dir.mkdir(parents=True, exist_ok=True)
single_lexicon_dirs = []

full_graph_json = {
    "nodes": {},
    "edges": []
}
for category in categories:
    for triple_amount in triple_amounts:
        # for some reason only 1triples has "_allSolutions"
        if triple_amount == "1triples":
            data_segment_dir = f"{category}_allSolutions"
        else:
            data_segment_dir = f"{category}"

        data_path = Path(
            f"../pogg_formatted_data_stash/dev/{triple_amount}/{data_segment_dir}/graphs/modified_triplesets/json/")

        # load data from graph json
        graph_json_path = Path(data_path, f"{category}_full_graph_format.json")
        with open(graph_json_path, "r") as f:
            latest_graph_json = json.load(f)

            # delete gold_lexicalizations -- we don't need them for this AND the ids are not unique across files
            del latest_graph_json["gold_lexicalizations"]

            ###
            # create / update lexicon for single file
            single_lexicon_path = Path(f"../pogg_formatted_data_stash/dev/{triple_amount}/{data_segment_dir}/lexicon")
            single_lexicon_path.mkdir(parents=True, exist_ok=True)
            single_lexicon_dirs.append(single_lexicon_path)
            single_lexicon_skeleton = POGGLexiconUtil.create_lexicon_skeleton(latest_graph_json)

            # Initialize directory (POGGLexiconUtil.initialize_directory will not overwrite files if they exist)
            POGGLexiconUtil.initialize_lexicon_directory(category, single_lexicon_path, single_lexicon_skeleton)

            # expand any entries that have been filled in by user
            POGGLexiconUtil.update_lexicon_files(single_lexicon_path)
            ###


            for key in latest_graph_json['nodes']:
                full_graph_json['nodes'][key] = latest_graph_json['nodes'][key]
            for edge in latest_graph_json['edges']:
                full_graph_json['edges'].append(edge)


# create skeleton from all data
lexicon_skeleton = POGGLexiconUtil.create_lexicon_skeleton(full_graph_json)

# Initialize directory (POGGLexiconUtil.initialize_directory will not overwrite files if they exist)
POGGLexiconUtil.initialize_lexicon_directory(lexicon_name, lexicon_dir, lexicon_skeleton)

# expand any entries that have been filled in by user
POGGLexiconUtil.update_lexicon_files(lexicon_dir, single_lexicon_dirs)
