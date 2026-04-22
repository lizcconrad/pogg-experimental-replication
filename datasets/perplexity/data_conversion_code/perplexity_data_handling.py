import re

def regularize_node(node_text):
    """
    Regularize nodes to remove the number at the end.
    For example, idApple1 and idApple2 should map to the same ERG predicate label, so remove the number to get idApple
    :param node_text: node text
    :type node_text: str
    :return: trimmed node text
    :rtype: str
    """
    matched = re.match("(id[A-z]+)[0-9]+$", str(node_text))
    # if a match is found, just return the capture group
    if matched:
        return matched.group(1)
    # if not, it might just be a property, or it couldn't be regularized,
    # so just try to return it
    else:
        return str(node_text)

def regularize_edge(edge_text):
    """
    Regularize property to get just the property name, trimming the object its associated with
    For example, idObject1_prop_idProperty should return idProperty
    :param edge_text: edge text
    :type edge_text: str
    :return: trimmed edge text
    :rtype: str
    """
    matched = re.search("prop_([A-z]+)", str(edge_text))
    # if a match is found, just return the capture group
    if matched:
        return matched.group(1)
    # if not, it couldn't be regularized,
    # so just try to return it
    else:
        return str(edge_text)

def convert_data_instance_to_json(data_instance):
    """
    Input data shape:
    {'Entity': 'idGlowingGrass1',
        'Properties': [
            {'args': ['idGlowingGrass1_prop_idColor', 'green'], 'functor': ','}
        ],
        'Relationships': [
            {'args': ['idGlowingGrass1', {'args': ['isTouching', 'idGlowingArea1'], 'functor': ','}], 'functor': ','}
        ]
    }

    Output data shape:
    {
        'nodes': {
            "idGlowingGrass1": {
                node_properties: {
                    node_type: "entity"
                    lexicon_key: "idGlowingGrass"
                }
            },
            "green": {
                node_properties: {
                    node_type: "property"
                }
            },
            "idGlowingArea1"
        },
        'edges': [
            {
                "edge_name": "idGlowingGrass1_prop_idColor",
                "parent_node": "idGlowingGrass1",
                "child_node": "green",
                "edge_properties": {
                    "edge_type": "property",
                    "lexicon_key": "idColor"
                }
            },
            {
                "edge_name": "isTouching",
                "parent_node": "idGlowingGrass1",
                "child_node": "idGlowingArea1",
                "edge_properties": {
                    "edge_type": "relationship"
                }
            }
        ]
    }
    """

    # graph_json can be appended to if you want a large graph or just start with it empty
    graph_json = {
        'nodes': {},
        'edges': []
    }

    # add node for Entity name to set
    entity_name = data_instance['Entity']
    if entity_name not in graph_json['nodes'].keys():
        graph_json['nodes'][data_instance['Entity']] = {}
        graph_json['nodes'][entity_name] = {
            "lexicon_key": regularize_node(entity_name),
            "node_properties": {
                "node_type": "entity"
            }
        }

    for prop in data_instance['Properties']:
        # parent node is entity_name
        # get edge and child node
        edge_name = prop['args'][0]

        # if child_node not already in set of nodes, add it
        # not setting lexicon_key because for properties it's usually just the property name itself
        child_node_value = prop['args'][1]
        # sometimes property values are a list (???)
        # so check if it's a list and if not just make it a list of one and loop over it
        # adding an edge from parent to each value in the list
        if not isinstance(child_node_value, list):
            child_node_value = [child_node_value]
        for child_node in child_node_value:
            if child_node not in graph_json['nodes'].keys():
                graph_json['nodes'][child_node] = {
                    "node_properties": {
                        "node_type": "property"
                    }
                }

            graph_json['edges'].append({
                "edge_name": edge_name,
                "parent_node": entity_name,
                "child_node": child_node,
                "lexicon_key": regularize_edge(edge_name),
                "edge_properties": {
                    "edge_type": "property"
                }
            })


    # add edges from Relationships
    for rel in data_instance['Relationships']:
        # parent node is entity_name
        # get edge and child node
        # {'args': ['idGlowingGrass1', {'args': ['isTouching', 'idGlowingArea1'], 'functor': ','}], 'functor': ','}
        edge_name = rel['args'][1]['args'][0]


        # if child_node not already in set of nodes, add it
        child_node = rel['args'][1]['args'][1]
        if child_node not in graph_json['nodes'].keys():
            graph_json['nodes'][child_node] = {
                "lexicon_key": regularize_node(child_node),
                "node_properties": {
                    "node_type": "entity"
                }
            }

        graph_json['edges'].append({
            "edge_name": edge_name,
            "parent_node": entity_name,
            "child_node": child_node,
            "lexicon_key": regularize_edge(edge_name),
            "edge_properties": {
                "edge_type": "relationship"
            }
        })


    return graph_json