import os
from types import ModuleType
import unittest
import tempfile

from pixie.genparser import generatePixieParserModule


class TestPixieGrammar(unittest.TestCase):
    tempFile: tempfile._TemporaryFileWrapper
    parserModule: ModuleType

    @classmethod
    def setUpClass(cls):
        script_dir = os.path.dirname(__file__)
        grammar_file_path = "../pixie/grammar/pypixie.gram"
        grammar_file = os.path.join(script_dir, grammar_file_path)
        module = generatePixieParserModule(grammar_file)
        assert module is not None
        TestPixieGrammar.parserModule = module

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

    def test_passComponentAsProp(self):
        input = """
w=<World/>
c=<Hello greet={w}>
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
