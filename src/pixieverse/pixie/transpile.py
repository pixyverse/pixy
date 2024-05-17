import ast

"""This is a reference to a generated parser. Generate it using
python -m pegen ./src/pixieverse/pixie/grammar/pypixie.gram -o src/pixieverse/pixie/parser.py
"""
from pixieverse.pixie.parser import parse_string


def transpile_source_tomodule(source: str) -> ast.Module:
    return parse_string(source, mode="exec")


def transpile_source(source: str) -> str:
    return ast.unparse(transpile_source_tomodule(source))
