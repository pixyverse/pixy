import importlib.util
from importlib.machinery import SourceFileLoader
import sys
import string
import secrets
import os
from types import ModuleType
import unittest
import tempfile

from pixie.genparser import generatePixieParser


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


class TestPixieGrammar(unittest.TestCase):
    tempFile: tempfile._TemporaryFileWrapper
    parserModule: ModuleType | None

    @classmethod
    def setUpClass(cls):
        script_dir = os.path.dirname(__file__)
        grammar_file_path = "../pixie/grammar/pypixie.gram"
        grammar_file = os.path.join(script_dir, grammar_file_path)
        parsy = generatePixieParser(grammar_file)
        parsy.seek(0)
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            while bite := parsy.read():
                fp.write(bytes(bite, encoding="utf-8"))
                fp.close()
        TestPixieGrammar.tempFile = fp
        TestPixieGrammar.parserModule = load_module(fp.name)

    @classmethod
    def tearDownClass(cls):
        TestPixieGrammar.tempFile.close()
        TestPixieGrammar.parserModule = None

    def test_simplePyIsValidPixie(self):
        testcases = [
            ("single_line", "a = 1;print(a)"),
            (
                "proper_indent",
                """
a += 1
print(a)
""",
            ),
            ("empty_is_ok", ""),
        ]
        for testcase in testcases:
            with self.subTest(msg=testcase[0]):
                try:
                    TestPixieGrammar.parserModule.parse_string(testcase[1], mode="exec")
                except SyntaxError:
                    self.fail("No exception expected")

    def test_invalidPyReportsBroken(self):
        assert TestPixieGrammar.parserModule is not None
        testcases = [
            ("single_line", "a = 1print(a)"),
            (
                "proper_indent",
                """
a += 1
    print(a)
""",
            ),
            ("unfinished_business", "-"),
        ]
        for testcase in testcases:
            with self.subTest(msg=testcase[0]):
                self.assertRaises(
                    SyntaxError,
                    TestPixieGrammar.parserModule.parse_string,
                    testcase[1],
                    mode="exec",
                )

    def test_psxAssignment(self):
        assert TestPixieGrammar.parserModule is not None
        testcases = [
            ("assign_closed_element", "a=<Hello/>"),
            ("assign_block_element", "a=<Hello></Hello>"),
        ]
        for testcase in testcases:
            with self.subTest(msg=testcase[0]):
                try:
                    TestPixieGrammar.parserModule.parse_string(testcase[1], mode="exec")
                except SyntaxError:
                    self.fail("No exception expected")

    def test_ComponentAttributes(self):
        assert TestPixieGrammar.parserModule is not None
        testcases = [
            ("attribute_val", "<Victory claps={10}/>"),
            ("void_attribute", "<Button disabled/>"),
            (
                "block_attribute",
                "<Layout grid={(10,10)}><Nested palette={'RGB'}/></Layout>",
            ),
            ("attribute_expression", "<Grid Width={200+300}></Grid>"),
        ]
        for testcase in testcases:
            with self.subTest(msg=testcase[0]):
                try:
                    TestPixieGrammar.parserModule.parse_string(testcase[1], mode="exec")
                except SyntaxError:
                    self.fail("No exception expected")

    def test_nestedComponents(self):
        input = """
c=<Hello>
<World/>
</Hello>
"""
        try:
            TestPixieGrammar.parserModule.parse_string(input, mode="exec")
        except SyntaxError:
            self.fail("No exception expected")

    def test_invalidPixieComponentsFail(self):
        testcases = [
            ("broken_selfclose", "<Victory claps={10}>"),
            ("mismatched_tagname", "<Hello></ello>"),
        ]
        for testcase in testcases:
            with self.subTest(msg=testcase[0]):
                self.assertRaises(
                    SyntaxError,
                    TestPixieGrammar.parserModule.parse_string,
                    testcase[1],
                    mode="exec",
                )


if __name__ == "__main__":
    unittest.main()
