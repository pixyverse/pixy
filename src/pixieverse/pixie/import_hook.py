import ast
import sys
import os.path
from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location
from pixieverse.pixie.parser import parse_file
import logging

logger = logging.getLogger(__name__)


class PixieLoader(Loader):
    def __init__(self, filename):
        self.filename = filename

    def create_module(self, spec):
        logger.info(f"Custom Loader creating module {spec.origin}")
        try:
            parsed_module = parse_file(spec.origin)
            return parsed_module
        except SyntaxError as serr:
            print(serr)
        except NameError as nerr:
            print(nerr)
        except ImportError as ierr:
            print(ierr)

    def exec_module(self, module):
        ast.fix_missing_locations(module)
        transpiled = compile(module, filename="tmp.py", mode="exec")
        logging.debug(f"Transpiled: {transpiled}")
        exec(transpiled, vars(module))


class PixieFinder(MetaPathFinder):
    def find_spec(self, fullname: str, path, target=None):
        logger.debug(f"PixieFinder {fullname}, {path}")
        if path is not None or fullname is not None:
            if fullname.startswith("pix.") or fullname.endswith(".pix"):
                if "." in fullname:
                    *parents, name = fullname.split(".")
                for entry in path:
                    filename = os.path.join(entry, fullname)
                    logger.debug(f"Trying to load filename {filename}")
                    if os.path.exists(filename):
                        return spec_from_file_location(
                            fullname, filename, loader=PixieLoader(filename)
                        )
            else:
                filename = os.path.join(os.getcwd(), fullname + ".pix")
                logger.debug(f"Trying to load pixy filename {filename}")
                if os.path.exists(filename):
                    spec = spec_from_file_location(
                        fullname,
                        filename,
                        loader=PixieLoader(filename),
                        submodule_search_locations=[],
                    )
                    logger.debug(spec)
                    return spec
                else:
                    return None

        return None  # We don't know how to import this


def install_pix_ext_hook():
    """Inserts the .pix finder and loader into the import machinery"""
    logger.info("Installing .pix file finder and loader")
    sys.meta_path.append(PixieFinder())


# Install the custom finder and loader
install_pix_ext_hook()
