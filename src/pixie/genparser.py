from pegen.build import build_parser
from pegen.validator import validate_grammar
from pegen.python_generator import PythonParserGenerator
from pegen.parser_generator import ParserGenerator
from io import StringIO


def generatePixieParser(grammarPath: str):
    outputPath = StringIO()
    grammar, _, _ = build_parser(grammarPath)
    validate_grammar(grammar)
    gen: ParserGenerator = PythonParserGenerator(grammar, outputPath)
    gen.generate(grammarPath)
    return outputPath
