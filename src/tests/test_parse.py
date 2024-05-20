import os
from types import ModuleType
import unittest

from pixyverse.pixy.genparser import generatePixieParserModule


class TestPixyGrammar(unittest.TestCase):
    parserModule: ModuleType

    @classmethod
    def setUpClass(cls) -> None:
        module = generatePixieParserModule()
        assert module is not None
        TestPixyGrammar.parserModule = module

    def test_simplePyIsValidPixie(self) -> None:
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
                    TestPixyGrammar.parserModule.parse_string(testcase[1], mode="exec")
                except SyntaxError:
                    self.fail("No exception expected")

    def test_invalidPyReportsBroken(self) -> None:
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
                    TestPixyGrammar.parserModule.parse_string,
                    testcase[1],
                    mode="exec",
                )

    def test_psxAssignment(self) -> None:
        testcases = [
            ("assign_closed_element", "a=<Hello/>"),
            ("assign_block_element", "a=<Hello></Hello>"),
        ]
        for testcase in testcases:
            with self.subTest(msg=testcase[0]):
                try:
                    TestPixyGrammar.parserModule.parse_string(testcase[1], mode="exec")
                except SyntaxError:
                    self.fail("No exception expected")

    def test_ComponentAttributes(self) -> None:
        testcases = [
            ("attribute_val", "<Victory claps={10}/>"),
            ("plain_string", "<p title='Hover Here'></p>"),
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
                    TestPixyGrammar.parserModule.parse_string(testcase[1], mode="exec")
                except SyntaxError:
                    self.fail("No exception expected")

    def test_nestedComponents(self) -> None:
        input = """
c=<Hello>
<World/>
</Hello>
"""
        try:
            TestPixyGrammar.parserModule.parse_string(input, mode="exec")
        except SyntaxError:
            self.fail("No exception expected")

    def test_passComponentAsProp(self) -> None:
        input = """
w=<World/>
c=<Hello greet={w}>
</Hello>
"""
        try:
            TestPixyGrammar.parserModule.parse_string(input, mode="exec")
        except SyntaxError:
            self.fail("No exception expected")

    def test_ExpressionsInBlockElement(self) -> None:
        input = """
c=<Hello>
{1+2}
{True}
</Hello>
"""
        try:
            TestPixyGrammar.parserModule.parse_string(input, mode="exec")
        except SyntaxError:
            self.fail("No exception expected")

    def test_GenExpressionsInBlockElement(self) -> None:
        input = """
names = ['Alice','Bob','Charlie']
c=<Hello>
<ul>
{map(lambda name: <li>{name}</li>, names)}
</ul>
</Hello>
"""
        try:
            TestPixyGrammar.parserModule.parse_string(input, mode="exec")
        except SyntaxError:
            self.fail("No exception expected")

    def test_LiteralStringsInBlockElement(self) -> None:
        input = """
c=<Hello>
"This is a literal string"
</Hello>
"""
        try:
            TestPixyGrammar.parserModule.parse_string(input, mode="exec")
        except SyntaxError:
            self.fail("No exception expected")

    def test_invalidPixieComponentsFail(self) -> None:
        testcases = [
            ("broken_selfclose", "<Victory claps={10}>"),
            ("mismatched_tagname", "<Hello></ello>"),
        ]
        for testcase in testcases:
            with self.subTest(msg=testcase[0]):
                self.assertRaises(
                    SyntaxError,
                    TestPixyGrammar.parserModule.parse_string,
                    testcase[1],
                    mode="exec",
                )

    def test_invalidPixieComponentsErrorReport(self) -> None:
        testcases = [
            ("broken_selfclose_1", "./data/invalid0.pix"),
            ("broken_selfclose_2", "./data/invalid1.pix"),
            ("mismatched_tagname", "./data/invalid2.pix"),
        ]
        for testcase in testcases:
            TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), testcase[1])
            with self.subTest(msg=testcase[0]):
                if testcase[0] == "broken_selfclose_1":
                    self.skipTest("pegen parser throws error in invalid line number and fails")
                try:
                    TestPixyGrammar.parserModule.parse_file(TESTDATA_FILENAME)
                except SyntaxError as err:
                    print(err)


if __name__ == "__main__":
    unittest.main()
