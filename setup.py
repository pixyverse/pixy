from contextlib import suppress
import logging
from pathlib import Path
from setuptools import Command, setup
from setuptools.command.build import build
import os


class CustomCommand(Command):
    def initialize_options(self) -> None:
        self.bdist_dir: Path | None = None

    def finalize_options(self) -> None:
        with suppress(Exception):
            bdist_command = self.get_finalized_command("bdist_wheel")
            if hasattr(bdist_command, "bdist_dir"):
                self.bdist_dir = Path(getattr(bdist_command, "bdist_dir"))

    def run(self) -> None:
        self.announce("Generate parser.py ...", level=logging.INFO)
        if self.bdist_dir:
            self.bdist_dir.mkdir(parents=True, exist_ok=True)
            self.mkpath(os.path.join(self.bdist_dir, "pixieverse", "pixie"))
            self.spawn(
                [
                    "python",
                    "-m",
                    "pegen",
                    "./src/pixieverse/pixie/grammar/pypixie.gram",
                    "-o",
                    os.path.join(self.bdist_dir, "pixieverse", "pixie", "parser.py"),
                ]
            )
            self.announce("Generated parser.py", logging.INFO)


class CustomBuild(build):
    sub_commands = [("build_custom", None)] + build.sub_commands


setup(cmdclass={"build": CustomBuild, "build_custom": CustomCommand})
