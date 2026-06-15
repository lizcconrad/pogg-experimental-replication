import json
from pathlib import Path
import xml.etree.ElementTree as ElementTree
from pogg.data_handling import POGGGraphUtil


web_nlg_parent_dir = Path("../webnlg-dataset-master/release_v3.0/en")
data_split = "dev"
num_triples = "2triples"

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

for category in categories:
    print(category)
    if num_triples == "1triples":
        file = f"{category}_allSolutions.xml"
    else:
        file = f"{category}.xml"

    xml_filepath = Path(web_nlg_parent_dir, data_split, num_triples, file)
    tree = ElementTree.parse(xml_filepath)

    graph_json_dir = Path("../pogg_formatted_data", data_split, num_triples, Path(file).stem, "graphs")
    m_graph_json_dir = Path(graph_json_dir, "modified_triplesets/json")
    m_graph_json_dir.mkdir(parents=True, exist_ok=True)

    # also create .dot files for all graphs
    m_graph_dot_dir = Path(graph_json_dir, "modified_triplesets/dot")
    m_graph_dot_dir.mkdir(parents=True, exist_ok=True)

    # and .txt files for gold outputs
    m_graph_gold_outputs = Path(graph_json_dir, "modified_triplesets/gold_outputs")
    m_graph_gold_outputs.mkdir(parents=True, exist_ok=True)

    entries_root = tree.getroot()[0]

    for entry in entries_root:
        category = entry.attrib["category"]
        entry_id = entry.attrib["eid"]
        shape = entry.attrib["shape"]
        shape_type = entry.attrib["shape_type"]
        size = entry.attrib["size"]

        modified_triples = []
        lexes = []
        for child in entry:
            if child.tag == "modifiedtripleset":
                for triple in child:
                    triple_string = triple.text
                    modified_triples.append(triple_string.split(" | "))
            elif child.tag == "lex":
                lex = {
                    "comment": child.attrib["comment"],
                    "lex_id": child.attrib["lid"],
                    "text": child.text
                }
                lexes.append(lex)

        m_graph_json = {
            "nodes": {},
            "edges": [],
            "original_gold_lex_dicts": {},
            "gold_outputs": set()
        }

        for triple in modified_triples:
            m_graph_json['nodes'][triple[0]] = {"lexicon_key": triple[0]}
            m_graph_json['nodes'][triple[2]] = {"lexicon_key": triple[2]}
            m_graph_json['edges'].append({
                "edge_name": triple[1],
                "parent_node": triple[0],
                "child_node": triple[2],
                "edge_properties": {
                    "lexicon_key": triple[1],
                }
            })

        for lex in lexes:
            m_graph_json['original_gold_lex_dicts'][lex["lex_id"]] = lex
            m_graph_json['original_gold_lex_dicts'][lex["lex_id"]].pop("lex_id")
            if lex["comment"] == "good":
                m_graph_json['gold_outputs'].add(lex["text"])

        m_graph_json['gold_outputs'] = sorted(list(m_graph_json['gold_outputs']))


        # dump JSON version of graph
        m_out = Path(m_graph_json_dir, f"{category}_{entry_id}.json")
        with open(m_out, mode="w", encoding="utf-8") as m_f:
            json.dump(m_graph_json, m_f, indent=4)

        # build graph then write to .dot
        m_graph = POGGGraphUtil.build_graph(m_graph_json)
        m_dot_out = Path(m_graph_dot_dir, f"{category}_{entry_id}.dot")
        with open(m_dot_out, mode="w", encoding="utf-8") as m_f:
            POGGGraphUtil.write_graph_to_dot(m_graph, m_dot_out)

        # dump gold outputs to txt file
        m_gold_out = Path(m_graph_gold_outputs, f"{category}_{entry_id}.txt")
        with open(m_gold_out, mode="w", encoding="utf-8") as m_g_f:
                m_g_f.writelines([f"{lex['text']}\n" for lex in lexes])

