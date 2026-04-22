import re

camel_case_pattern = r'(?<=[a-z])(?=[A-Z])'
snake_case_pattern = r',*_'
parse_pattern = camel_case_pattern

# perplexity
# idShinyRock -> shiny rock
def perplexity(x):
    # remove "id" if it's there
    x = re.sub("^id", "", x)

    tokens = [t.lower() for t in re.split(camel_case_pattern, x)]
    return " ".join(tokens)

# WebNLG
# Russian_Football_League -> Russian Football League
def webnlg(x):
    tokens = [t.lower() for t in re.split(snake_case_pattern, x)]
    return " ".join(tokens)

