import ast
from pixieverse.pixie.genparser import generatePixieParserModule


def transpile_source_tomodule(source: str) -> ast.Module:
    module = generatePixieParserModule()
    return module.parse_string(source, mode="exec")


def transpile_source(source: str) -> str:
    return ast.unparse(transpile_source_tomodule(source))
