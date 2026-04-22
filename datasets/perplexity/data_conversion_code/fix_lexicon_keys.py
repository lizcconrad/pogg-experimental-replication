import json
import os
import random
from pathlib import Path
from pogg.data_handling.graph_util import POGGGraphUtil
from perplexity_data_handling import regularize_node

mode = "test"
game = "Scenario"

full_graph_json_filepath = f"../{mode}/{game}/graphs/{game}_full_graph_format.json"
subgraphs_path = f"../{mode}/{game}/graphs/subgraphs"

json_path = Path(subgraphs_path, "json")
dot_path = Path(subgraphs_path, "dot")
png_path = Path(subgraphs_path, "png")

json_path.mkdir(parents=True, exist_ok=True)
dot_path.mkdir(parents=True, exist_ok=True)
png_path.mkdir(parents=True, exist_ok=True)


with open(full_graph_json_filepath, "r") as json_file:
    full_graph_json = json.load(json_file)

for graph in os.listdir(json_path):
    if graph.endswith(".json"):
        graph_json = json.load(open(Path(json_path, graph), "r"))

        # if it has edge information by mistake...
        for node_key in graph_json['nodes']:
            str_node_key = str(node_key)

            real_node_info = full_graph_json['nodes'][str_node_key]


            # if "edge_type" in graph_json['nodes'][str_node_key]:
            graph_json['nodes'][str_node_key] = {
                "lexicon_key": "",
                "node_properties": {}
            }

            for key in real_node_info['node_properties']:
                str_key = str(key)
                graph_json['nodes'][str_node_key]['node_properties'][str_key] = real_node_info['node_properties'][str_key]

            if "lexicon_key" not in real_node_info:
                graph_json['nodes'][str_node_key]['lexicon_key'] = regularize_node(str_node_key)
            else:
                graph_json['nodes'][str_node_key]['lexicon_key'] = real_node_info['lexicon_key']

            # graph_json['nodes'][str_node_key]['lexicon_key'] = real_node_info['lexicon_key']
            # del real_node_info['lexicon_key']
            # graph_json['nodes'][str_node_key]['node_properties'] = real_node_info

        # make sure all edge information is strings
        new_edges = []
        for edge in graph_json['edges']:
            new_edge = {}
            for key in edge:
                if isinstance(edge[str(key)], dict):
                    new_edge[key] = edge[str(key)]
                else:
                    new_edge[key] = str(edge[str(key)])
            new_edges.append(new_edge)

        graph_json['edges'] = new_edges

        with open(Path(json_path, graph), "w") as json_file:
            json.dump(graph_json, json_file, indent=4)




# making dot and gold output files
for item in os.listdir(json_path):
    print(item)
    if item.endswith(".json"):
        graph_name = Path(item).stem

        # make dot file
        graph_json = json.load(open(Path(json_path, item)))
        graph = POGGGraphUtil.build_graph(graph_json)
        POGGGraphUtil.write_graph_to_dot(graph, Path(dot_path, f"{graph_name}.dot"))
        POGGGraphUtil.write_graph_to_png(graph, Path(png_path, f"{graph_name}.png"))
