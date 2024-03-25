import importlib.util
from importlib.machinery import SourceFileLoader
import os
import secrets
import string
import sys
import tempfile
from types import ModuleType
from pegen.build import build_parser
from pegen.validator import validate_grammar
from pegen.python_generator import PythonParserGenerator
from pegen.parser_generator import ParserGenerator
from io import StringIO
from importlib.resources import as_file, files


def generatePixieParser(grammarPath: str):
    outputPath = StringIO()
    grammar, _, _ = build_parser(grammarPath)
    validate_grammar(grammar)
    gen: ParserGenerator = PythonParserGenerator(grammar, outputPath)
    gen.generate(grammarPath)
    return outputPath


def gensym(length=32, prefix="gensym_"):
    """
    generates a fairly unique symbol, used to make a module name,
    used as a helper function for load_module

    :return: generated symbol
    """
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    symbol = "".join([secrets.choice(alphabet) for i in range(length)])

    return prefix + symbol


def load_module(source, module_name=None):
    """
    reads file source and loads it as a module

    :param source: file to load
    :param module_name: name of module to register in sys.modules
    :return: loaded module
    """

    if module_name is None:
        module_name = gensym()

    loader = SourceFileLoader(module_name, source)
    spec = importlib.util.spec_from_file_location(module_name, loader=loader)
    if spec is not None:
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        if spec.loader is not None:
            spec.loader.exec_module(module)
        return module
    return None


def generatePixieParserModule() -> ModuleType:

    module = None
    grammar_file_context = as_file(
        files("pixieverse.pixie.grammar").joinpath("pypixie.gram")
    )
    with grammar_file_context as grammar_file:
        parsy = generatePixieParser(str(grammar_file))
        parsy.seek(0)
        with tempfile.NamedTemporaryFile() as fp:
            while bite := parsy.read():
                fp.write(bytes(bite, encoding="utf-8"))
            module = load_module(fp.name)
    assert module is not None
    return module
