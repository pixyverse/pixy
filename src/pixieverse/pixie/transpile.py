from astor.codegen import to_source

from pixieverse.pixie.genparser import generatePixieParserModule


def transpile_source(source: str):
    module = generatePixieParserModule()
    code = module.parse_string(source, mode="exec")
    return to_source(code)
