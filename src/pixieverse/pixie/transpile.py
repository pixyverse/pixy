import ast
import typing

"""This is a reference to a generated parser. Generate it using
python -m pegen ./src/pixieverse/pixie/grammar/pypixie.gram -o src/pixieverse/pixie/parser.py
"""
from pixieverse.pixie.parser import parse_string


def transpile_source_tomodule(source: str) -> ast.AST | None:
    return typing.cast(ast.AST | None, parse_string(source, mode="exec"))


def transpile_source(source: str) -> str | None:
    ast_module = transpile_source_tomodule(source)
    if ast_module:
        return ast.unparse(ast_module)
    return None
