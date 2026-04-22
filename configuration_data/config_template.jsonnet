function(input) {

    dataset_name: input.dataset_name,
    experimental_setups: input.experimental_setups,

    local inherited_external_lexicons =
        (if !std.objectHas(input, "inherited_external_lexicons") then
            []
        else [std.rstripChars(x, "/") for x in input.inherited_external_lexicons]),

    local data_dir_val =
        (if !std.objectHas(input, "data_dir") then
            "./evaluation"
        else input.data_dir ),

    local evaluation_dir_val =
        (if !std.objectHas(input, "evaluation_dir") then
            "./evaluation"
        else input.evaluation_dir),

    evaluation_run_anchor: std.join("/", [evaluation_dir_val, "EXPERIMENT_RUN_PLACEHOLDER"]),

    local lexicon_dir_val =
        (if !std.objectHas(input, "lexicons_dir") then
            "./lexicons"
        else input.lexicons_dir),

    local graph_rel_dir_val =
        (if !std.objectHas(input, "graph_rel_dir") then
            "graphs"
        else input.graph_rel_dir),

    data_dir: std.rstripChars(data_dir_val, "/"),
    evaluation_dir: std.rstripChars(evaluation_dir_val, "/"),
    lexicon_dir: std.rstripChars(lexicon_dir_val, "/"),
    graph_rel_dir: std.rstripChars(graph_rel_dir_val, "/"),

    # function to populate split data
    local Split(name, parent=null, leaf=false) =
        local parent_info = {
            [setup]: {
                parent_full_split_name: (
                    if parent != null then
                        parent.experiments[setup].full_data_split_name
                    else $.dataset_name
                ),
                parent_data_dir: (
                    if parent != null then
                        parent.experiments[setup].experiment_data_dir
                    else $.data_dir
                ),
                parent_eval_dir: (
                    if parent != null then
                        parent.experiments[setup].experiment_eval_dir
                    else std.join("_", [$.evaluation_run_anchor, setup])
                ),
                parent_lex_dir: (
                    if parent != null then
                        parent.experiments[setup].experiment_lex_dir
                    else std.join("/", [$.lexicon_dir, $.experimental_setups[setup]["lexicon_name"]])
                ),
            }
            for setup in std.objectFields($.experimental_setups)
        };
    {
        experiments: {
            [setup]: {
                experiment_name: setup,
                lexicon_name: $.experimental_setups[setup]["lexicon_name"],
                SEMENT_processing: $.experimental_setups[setup]["SEMENT_processing"],
                result_processing: $.experimental_setups[setup]["result_processing"],
                full_data_split_name: std.join("_", [parent_info[setup].parent_full_split_name, name]),
                experiment_data_dir: std.join("/", [parent_info[setup].parent_data_dir, name]),
                experiment_eval_dir: std.join("/", [parent_info[setup].parent_eval_dir, name]),
                experiment_lex_dir: std.join("/", [parent_info[setup].parent_lex_dir, name]),
                inherited_lexicons: (
                    # inherited external lexicons
                    [x for x in inherited_external_lexicons] +
                    # inherited lexicons from the same config
                    if std.objectHas($.experimental_setups[setup], "inherited_experiment_lexicons") then
                        [std.strReplace(self.experiment_lex_dir, setup, x)
                            for x in $.experimental_setups[setup]["inherited_experiment_lexicons"]]
                    else []
                )
            } + (
                if leaf then {
                    leaf: true,
                    graph_json_dir: std.join("/", [self.experiment_data_dir, graph_rel_dir_val, "json"]),
                    graph_dot_dir: std.join("/", [self.experiment_data_dir, graph_rel_dir_val, "dot"]),
                    graph_png_dir: std.join("/", [self.experiment_data_dir, graph_rel_dir_val, "png"])
                } else {
                    leaf: false
                }
            ),
            for setup in std.objectFields($.experimental_setups)
        }
    },

    # recursively call Split fxn for as many nested splits as necessary
    local SplitStructure(split_dict, parent=null) = (
        if std.isObject(split_dict) then {

            # if the name (x) matches the dataset name, then don't pass it in
            # this is to avoid inserting the "synthesized" top-level split into the path name
            [x]: (if x == $.dataset_name then Split(null, parent) else Split(x, parent)) + {
                splits: SplitStructure(split_dict[x], self)
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