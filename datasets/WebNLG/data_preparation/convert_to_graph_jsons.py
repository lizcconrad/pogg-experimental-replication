import json
from pathlib import Path
import xml.etree.ElementTree as ElementTree
from pogg.data_handling.graph_util import POGGGraphUtil


web_nlg_parent_dir = Path("../webnlg-dataset-master/release_v3.0/en")
data_split = "dev"
num_triples = "2triples"

categories = [
    "Airport",
    # "Artist",
    # "Astronaut",
    # "Athlete",
    # "Building",
    # "CelestialBody",
    # "City",
    # "ComicsCharacter",
    # "Company",
    # "Food",
    # "MeanOfTransportation",
    # "Monument",
    # "Politician",
    # "SportsTeam",
    # "University",
    # "WrittenWork"
]

for category in categories:
    print(category)
    # file = f"{category}_allSolutions.xml"
    file = f"{category}.xml"

    xml_filepath = Path(web_nlg_parent_dir, data_split, num_triples, file)
    tree = ElementTree.parse(xml_filepath)

    graph_json_dir = Path("../pogg_formatted_data_stash", data_split, num_triples, Path(file).stem, "graphs")
    o_graph_json_dir = Path(graph_json_dir, "original_triplesets/json")
    m_graph_json_dir = Path(graph_json_dir, "modified_triplesets/json")
    o_graph_json_dir.mkdir(parents=True, exist_ok=True)
    m_graph_json_dir.mkdir(parents=True, exist_ok=True)

    # also create .dot files for all graphs
    o_graph_dot_dir = Path(graph_json_dir, "original_triplesets/dot")
    m_graph_dot_dir = Path(graph_json_dir, "modified_triplesets/dot")
    o_graph_dot_dir.mkdir(parents=True, exist_ok=True)
    m_graph_dot_dir.mkdir(parents=True, exist_ok=True)

    entries_root = tree.getroot()[0]
    o_master_graph_json = {
        "nodes": {},
        "edges": [],
        "gold_lexicalizations": []
    }

    m_master_graph_json = {
        "nodes": {},
        "edges": [],
        "gold_lexicalizations": []
    }

    for entry in entries_root:
        category = entry.attrib["category"]
        entry_id = entry.attrib["eid"]
        shape = entry.attrib["shape"]
        shape_type = entry.attrib["shape_type"]
        size = entry.attrib["size"]

        original_triples = []
        modified_triples = []
        lexes = []
        # TODO: THIS IS BROKEN... needs to loop over the children of the children for multiple triples
        for child in entry:
            if child.tag == "originaltripleset":
                triple_string = child[0].text
                original_triples.append(triple_string.split(" | "))
            elif child.tag == "modifiedtripleset":
                triple_string = child[0].text
                modified_triples.append(triple_string.split(" | "))
            elif child.tag == "lex":
                lex = {
                    "comment": child.attrib["comment"],
                    "lex_id": child.attrib["lid"],
                    "text": child.text
                }
                lexes.append(lex)

        o_graph_json = {
            "nodes": {},
            "edges": [],
            "gold_lexicalizations": []
        }
        m_graph_json = {
            "nodes": {},
            "edges": [],
            "gold_lexicalizations": []
        }

        triplesets = [original_triples, modified_triples]
        graph_jsons = [o_graph_json, m_graph_json]
        for i in range(len(triplesets)):
            graph_json = graph_jsons[i]

            for triple in triplesets[i]:
                graph_json['nodes'][triple[0]] = {"lexicon_key": triple[0]}
                graph_json['nodes'][triple[2]] = {"lexicon_key": triple[2]}
                graph_json['edges'].append({
                    "edge_name": triple[1],
                    "parent_node": triple[0],
                    "child_node": triple[2],
                    "edge_properties": {
                        "lexicon_key": triple[1],
                    }
                })

            for lex in lexes:
                graph_json['gold_lexicalizations'].append(lex)

        # dump JSON version of graph
        o_out = Path(o_graph_json_dir, f"{category}_{entry_id}.json")
        m_out = Path(m_graph_json_dir, f"{category}_{entry_id}.json")

        with open(o_out, mode="w", encoding="utf-8") as o_f:
            json.dump(o_graph_json, o_f, indent=4)

        with open(m_out, mode="w", encoding="utf-8") as m_f:
            json.dump(m_graph_json, m_f, indent=4)


        # build graphs then write to .dot
        o_graph = POGGGraphUtil.build_graph(o_graph_json)
        m_graph = POGGGraphUtil.build_graph(m_graph_json)

        o_dot_out = Path(o_graph_dot_dir, f"{category}_{entry_id}.dot")
        m_dot_out = Path(m_graph_dot_dir, f"{category}_{entry_id}.dot")

        with open(o_dot_out, mode="w", encoding="utf-8") as o_f:
            POGGGraphUtil.write_graph_to_dot(o_graph, o_dot_out)

        with open(m_dot_out, mode="w", encoding="utf-8") as m_f:
            POGGGraphUtil.write_graph_to_dot(m_graph, m_dot_out)

        # add to master json
        o_master_graph_json["nodes"].update(o_graph_json["nodes"])
        m_master_graph_json["nodes"].update(m_graph_json["nodes"])

        o_master_graph_json["edges"].extend(o_graph_json["edges"])
        m_master_graph_json["edges"].extend(m_graph_json["edges"])

        o_master_graph_json["gold_lexicalizations"].extend(o_graph_json["gold_lexicalizations"])
        m_master_graph_json["gold_lexicalizations"].extend(m_graph_json["gold_lexicalizations"])


    master_o_out = Path(o_graph_json_dir, f"{category}_full_graph_format.json")
    master_m_out = Path(m_graph_json_dir, f"{category}_full_graph_format.json")

    with open(master_o_out, mode="w", encoding="utf-8") as o_f:
        json.dump(o_master_graph_json, o_f, indent=4)

    with open(master_m_out, mode="w", encoding="utf-8") as m_f:
        json.dump(m_master_graph_json, m_f, indent=4)


