function(input) {

    dataset_name: input.dataset_name,
    experimental_setups: input.experimental_setups,

    local inherited_external_lexicons =
        (if !std.objectHas(input, "inherited_external_lexicons") then
            []
        else [std.rstripChars(x, "/") for x in input.inherited_external_lexicons]),

    local data_dir_val =
        (if !std.objectHas(input, "data_dir") then
            "./output"
        else input.data_dir ),

    local output_dir_val =
        (if !std.objectHas(input, "output_dir") then
            "./output"
        else input.output_dir),

    evaluation_run_anchor: std.join("/", [output_dir_val, "EXPERIMENT_RUN_PLACEHOLDER"]),

    local lexicon_dir_val =
        (if !std.objectHas(input, "lexicons_dir") then
            "./lexicons"
        else input.lexicons_dir),

    local graph_rel_dir_val =
        (if !std.objectHas(input, "graph_rel_dir") then
            "graphs"
        else input.graph_rel_dir),

    data_dir: std.rstripChars(data_dir_val, "/"),
    output_dir: std.rstripChars(output_dir_val, "/"),
    lexicon_dir: std.rstripChars(lexicon_dir_val, "/"),
    graph_rel_dir: std.rstripChars(graph_rel_dir_val, "/"),

    # lexicons
    lexicons: {
        [x]: {
            lexicon_dir: std.join("/", [$.lexicon_dir, x])
        }
        for x in input.lexicons
    },

    # function to populate split data
    local Split(name, parent=null, leaf=false) =
        local parent_split_info = {
            parent_full_split_name: (
                if parent != null then
                    parent.split_info.full_data_split_name
                else $.dataset_name
            ),
            parent_data_dir: (
                if parent != null then
                    parent.split_info.split_data_dir
                else $.data_dir
            ),
        };

        local parent_experiments = {
            [setup]: {
                parent_output_dir: (
                    if parent != null then
                        parent.experiments[setup].experiment_output_dir
                    else std.join("_", [$.evaluation_run_anchor, setup])
                )
            }
            for setup in std.objectFields($.experimental_setups)
        };
    {
        split_info: {
            full_data_split_name: std.join("_", [parent_split_info.parent_full_split_name, name]),
            data_split_path: std.split(self.full_data_split_name, "_"),
            split_data_dir: std.join("/", [parent_split_info.parent_data_dir, name]),
        } + (
            if leaf then {
                leaf: true,
                graph_json_dir: std.join("/", [self.split_data_dir, graph_rel_dir_val, "json"]),
                graph_dot_dir: std.join("/", [self.split_data_dir, graph_rel_dir_val, "dot"]),
                graph_png_dir: std.join("/", [self.split_data_dir, graph_rel_dir_val, "png"]),
                data_directories: [self.graph_json_dir]
            } else {
                leaf: false
            }
        ),
        experiments: {
            [setup]: {
                experiment_name: setup,
                lexicon_name: $.experimental_setups[setup]["lexicon_name"],
                SEMENT_processing: $.experimental_setups[setup]["SEMENT_processing"],
                result_processing: $.experimental_setups[setup]["result_processing"],
                experiment_output_dir: std.join("/", [parent_experiments[setup].parent_output_dir, name]),
                experiment_lex_dir: std.join("/", [$.lexicon_dir, $.experimental_setups[setup]["lexicon_name"]]),
                inherited_lexicons: (
                    # inherited external lexicons
                    [x for x in inherited_external_lexicons] +
                    # inherited lexicons from the same config
                    if std.objectHas($.experimental_setups[setup], "inherited_experiment_lexicons") then
                        [std.strReplace(self.experiment_lex_dir, setup, x)
                            for x in $.experimental_setups[setup]["inherited_experiment_lexicons"]]
                    else []
                )
            }
            for setup in std.objectFields($.experimental_setups)
        }
    },

    local DescendantDataDirectories(split_dict, parent_data_dir_val=null) = (
        if std.isObject(split_dict) then (
            // call recursively and flatten results from recursive calls
            local child_result_arrays = [
                DescendantDataDirectories(split_dict[x], std.join("/", [parent_data_dir_val, x]))
                for x in std.objectFields(split_dict)
            ];

            std.flattenArrays(child_result_arrays)
        ) else [std.join("/", [parent_data_dir_val, x, $.graph_rel_dir, "json"]) for x in split_dict]

    ),

    # recursively call Split fxn for as many nested splits as necessary
    local SplitStructure(split_dict, parent=null) = (
        if std.isObject(split_dict) then {
            # if the name (x) matches the dataset name, then don't pass it in
            # this is to avoid inserting the "synthesized" top-level split into the path name
            [x]: (
                if x == $.dataset_name then Split(null, parent) else Split(x, parent)
            ) + {
                splits: SplitStructure(split_dict[x], self)
            } + {
                # update data_directories (i.e. inherit split_info object and just add this field)
                split_info+: {
                    data_directories: DescendantDataDirectories(split_dict[x], self.split_data_dir)
                }
            }
            for x in std.objectFields(split_dict)
        } else {
            [x]: Split(x, parent, true)
            for x in split_dict
        }
    ),
    # wrap split_structure to get experiment info for full dataset
    local wrapped_split_structure = {
        [$.dataset_name]: input.split_structure
    },
    splits: SplitStructure(wrapped_split_structure)
}