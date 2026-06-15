import json

with open("post_perplexity_no_numbers_lexicon_approved_entries.json", "r") as f:
    approved_entries = json.load(f)

with open("post_perplexity_no_numbers_lexicon_all_entries.json", "r") as f:
    all_entries = json.load(f)

    for key, entry in approved_entries["node_entries"].items():
        if entry["flags"]["approved"]:
            all_entries["node_entries"][key]["flags"]["approved"] = True

with open("post_perplexity_no_numbers_lexicon_all_entries.json", "w") as f:
    json.dump(all_entries, f)