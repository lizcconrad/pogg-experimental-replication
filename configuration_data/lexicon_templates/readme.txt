perplexity_templates_initial_dump.json
    - templates automatically extracted from Perplexity lexicon
perplexity_templates.json
    - examples filled in
    - subset of templates from _initial_dump that excludes certain templates
    - some complex templates are excluded
        - this includes some that couldn't be "transparently" obtained from a direct parse of the node name
        - or some that I judged to be highly idiosyncratic
    - sometimes if the predicate label is known to be "unusual" I will replace it (and possibly update the template title)
        - e.g. _player_n_of has an ARG1, which is rarer than a noun with only ARG0, so I replace it
        - ideally there would be a way to have both versions of the template
        - ... OR recognize that the only difference between the ERG MRS and the template-generated MRS is an extra unfilled ARG
        - but for now if a pred's synopsis doesn't match what's in the template then it can't be auto-filled