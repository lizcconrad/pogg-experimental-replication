import sys
import re
import argparse
import string_processing

from pogg.pogg_routine import POGGExperimentConfig
from pogg.lexicon.auto_lexicon import POGGLexiconAutoFiller
from pogg.lexicon.lexicon_builder import POGGLexiconUtil


parser = argparse.ArgumentParser()
parser.add_argument("composition_config",  type=str, help="path to the config which specifies grammar information")
parser.add_argument("experiment_config",  type=str, help="path to the config which specifies experiments")

parser.add_argument("-a", "--auto_filling",  action="store_true", help="attempt to auto-fill lexicon if argument is provided")
parser.add_argument("-t", "--lexicon_template_files",  nargs="+", type=str, help="list of paths to files of lexicon entry templates")
parser.add_argument("-s", "--string_processing_fxn",  type=str, help="name of string processing function to use from string_processing.py")
parser.add_argument("-f", "--find_new_templates",  action="store_true", help="find new templates from lexicon to template file if argument is provided")
parser.add_argument("-d", "--dump_file",  type=str, help="file to dump new templates to; can be one of the files templates are being pulled from")

args = parser.parse_args()

composition_config = args.composition_config
experiment_config = args.experiment_config

auto_filling = args.auto_filling
find_new_templates = args.find_new_templates

if auto_filling or find_new_templates:
    if args.lexicon_template_files is None:
        raise Exception("When auto_filling, -t (--lexicon_templates) must be provided")
    if args.string_processing_fxn is None:
        raise Exception("When auto_filling, -s (--string_processing_fxn) must be provided")
    if not find_new_templates:
        if args.dump_file is None:
            raise Exception("When finding new templates, -d (--dump_file) must be provided")

    str_processing_fxn = getattr(string_processing, args.string_processing_fxn)
    lexicon_auto_filler = POGGLexiconAutoFiller(composition_config, args.lexicon_template_files, args.dump_file)



experiments = POGGExperimentConfig(composition_config, experiment_config)
lexicons = experiments.get_leaf_lexicons()
for lexicon in lexicons:
    if auto_filling:
        lexicon_auto_filler.attempt_auto_filling(lexicon, str_processing_fxn)

    lexicon.update_lexicon_files()
    ancestors = experiments.get_ancestor_lexicons(lexicon)
    POGGLexiconUtil.propagate_lexicon_changes(lexicon, ancestors)

    if find_new_templates:
        lexicon_auto_filler.dump_new_templates(lexicon)
