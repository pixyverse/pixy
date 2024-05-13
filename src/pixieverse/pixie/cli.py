import argparse
from pixieverse.pixie.transpile import transpile_source


cli_parser = argparse.ArgumentParser(
    prog="pixie",
    description="Parse and transpile pixie files to py files",
)
cli_parser.add_argument(
    "-p",
    "--pixfile",
    required=True,
    type=argparse.FileType("r"),
    help=".pix filename to parse and transpile to .py file",
)
cli_parser.add_argument(
    "-o", "--outputfile", type=argparse.FileType("w"), help="output .py filename"
)


def runtranspile():
    args = cli_parser.parse_args()
    if args.pixfile:
        with args.pixfile as inputfile:
            source = inputfile.read()
            transpiled = transpile_source(source)
            with args.outputfile as writer:
                writer.write(transpiled)
