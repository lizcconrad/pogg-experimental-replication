import re
import os
import pathlib
import json
from perplexity_data_handling import convert_data_instance_to_json

mode = "test"

raw_data_directory = f"/Users/lizcconrad/Documents/PhD/POGG/data_handling/perplexity/{mode}/data_jsons"
graph_data_directory = f"/Users/lizcconrad/Documents/PhD/POGG/data_handling/perplexity/{mode}/graph_jsons"

# Iterate over files in directory
raw_data_files = sorted([name for name in os.listdir(raw_data_directory)])
print(raw_data_files)

raw_data_files = ['AtomicCity_raw_data.json']

# for each "game world"...
for raw_data_json in raw_data_files:
    if raw_data_json.endswith(".json"):
        print(raw_data_json)
        game_name = re.match(r'(.*)_raw_data.json', raw_data_json).group(1)

        # mkdirs
        scenario_graph_dir = os.path.join(graph_data_directory, game_name)
        entity_graphs_dir = pathlib.Path(scenario_graph_dir, "entity_graphs")
        pathlib.Path(scenario_graph_dir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(entity_graphs_dir).mkdir(parents=True, exist_ok=True)

        full_graph_json = {
            'nodes': {},
            'edges': []
        }

        # write graph_json for just one entity in the "game world"
        with open(os.path.join(raw_data_directory, raw_data_json), "r") as raw_data_file:
            data = json.load(raw_data_file)

            for entry in data:
                single_graph_json = convert_data_instance_to_json(entry)
                single_graph_json_file_name = f"{entry['Entity']}_{game_name}_graph_format.json"
                with open(os.path.join(entity_graphs_dir, single_graph_json_file_name), "w") as entity_json_file:
                    json.dump(single_graph_json, entity_json_file, indent=4)
                full_graph_json['nodes'].update(single_graph_json['nodes'])
                full_graph_json['edges'].extend(single_graph_json['edges'])

        # write graph_json for whole "game world"
        with open(os.path.join(scenario_graph_dir, f"{game_name}_full_graph_format.json"), "w") as graph_json_file:
            json.dump(full_graph_json, graph_json_file, indent=4)