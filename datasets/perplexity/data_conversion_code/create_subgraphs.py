import json
import random
from pathlib import Path
from pogg.data_handling.graph_util import POGGGraphUtil

mode = "test"
game = "HealTheFlashback"

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

def add_child_nodes(subgraph_json, parent, child_nodes):
    for child in child_nodes:
        child_name, child_props = child[0], child[1]
        # add child to nodes
        subgraph_json["nodes"][child_name] = child_props

        parent_to_child_edge_data = graph.get_edge_data(parent, child_name)
        subgraph_json["edges"].append({
            "edge_name": parent_to_child_edge_data["label"],
            "parent_node": parent,
            "child_node": child_name,
            "lexicon_key": parent_to_child_edge_data["lexicon_key"],
            "edge_properties": {
                "edge_type": parent_to_child_edge_data["edge_type"],
            }
        })

# 1. all properties, up to 3
# 2. 0-1 relationships with other entities
# 3. all properties of other entity, up to 2

graph = POGGGraphUtil.build_graph(full_graph_json)

for node in graph.nodes(data=True):
    node_name, node_props = node[0], node[1]
    if node_name != "idKey1":
        continue

    if "node_type" in node_props and node_props["node_type"] == "entity":
        subgraph_json = {
            "nodes": {},
            "edges": []
        }

        # add subgraph root to nodes
        subgraph_json["nodes"][node_name] = node_props


        # get all children that are properties
        children = [child_name for child_name in graph.successors(node_name)]
        property_children = []
        entity_children = []

        for child in children:
            child_edge_data = graph.get_edge_data(node_name, child)
            if child_edge_data["edge_type"] == "property":
                property_children.append((child, graph.nodes[child]))
            elif child_edge_data["edge_type"] == "relationship":
                entity_children.append((child, graph.nodes[child]))
            else:
                print(f"unclassified child: {child}")

        if len(property_children) > 3:
            property_children = random.sample(property_children, 3)

        if len(entity_children) > 1:
            entity_children = random.sample(entity_children, 1)

        # add info to subgraph_json
        add_child_nodes(subgraph_json, node_name, property_children)
        add_child_nodes(subgraph_json, node_name, entity_children)

        # add the relationship edge
        if len(entity_children) == 1:
            chosen_entity = entity_children[0]
            chosen_entity_name, chosen_entity_props = chosen_entity[0], chosen_entity[1]
            subgraph_json["nodes"][chosen_entity_name] = chosen_entity_props

            # get all the property children of the chosen entity
            grandchildren = [child_name for child_name in graph.successors(chosen_entity_name)]
            property_grandchildren = []

            for grandchild in grandchildren:
                grandchild_edge_data = graph.get_edge_data(chosen_entity_name, grandchild)
                if grandchild_edge_data["edge_type"] == "property":
                    property_grandchildren.append((grandchild, graph.nodes[grandchild]))

            # choose random number from 0-2
            to_include = random.randrange(0, 3)
            if len(property_grandchildren) > to_include:
                property_grandchildren = random.sample(property_grandchildren, to_include)

            add_child_nodes(subgraph_json, chosen_entity_name, property_grandchildren)

        # dump subgraph.json
        with open(Path(json_path, f"{node_name}_subgraph.json"), "w") as json_file:
            json.dump(subgraph_json, json_file, indent=4)

        # make graph
        subgraph = POGGGraphUtil.build_graph(subgraph_json)

        # write dot file
        POGGGraphUtil.write_graph_to_dot(subgraph, Path(dot_path, f"{node_name}_subgraph.dot"))

        # write png file
        POGGGraphUtil.write_graph_to_png(subgraph, Path(png_path, f"{node_name}_subgraph.png"))