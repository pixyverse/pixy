import os
from astor.codegen import to_source

from pixieverse.pixie.genparser import generatePixieParserModule


def transpile_source(source: str):
    script_dir = os.path.dirname(__file__)
    grammar_file_path = "./grammar/pypixie.gram"
    grammar_file = os.path.join(script_dir, grammar_file_path)
    module = generatePixieParserModule(grammar_file)
    code = module.parse_string(source, mode="exec")
    return to_source(code)
