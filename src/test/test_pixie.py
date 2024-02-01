import unittest

from parsec import ParseError
from pixie.ast import (
    PSXAttributeInitializerNode,
    PSXAttributeNode,
    PSXBlockElementNode,
    PSXIdentiferNameNode,
)

from pixie.parse import (
    PSXAttribute,
    PSXAttributeInitializer,
    JSXElement,
    PSXIdentifier,
    PSXSelfClosingElement,
    PSXStringCharacters,
)


class TestPixie(unittest.TestCase):
    def test_jsxIdentifier(self):
        self.assertEqual(PSXIdentifier.parse("abc"), "abc")
        self.assertRaises(ParseError, PSXIdentifier.parse_strict, "ab<")

    def test_jsxSelfClosingElement(self):
        self.assertEqual(PSXSelfClosingElement.parse("<hello/>"), ("hello", []))
        self.assertRaises(
            ParseError, PSXSelfClosingElement.parse, ["<hello", "<hello/>"]
        )

    def test_jsxStringCharacter(self):
        self.assertEqual(PSXStringCharacters.parse_strict('"a"'), "a")
        self.assertEqual(PSXStringCharacters.parse_strict('"abc"'), "abc")
        self.assertRaises(ParseError, PSXStringCharacters.parse_strict, '"AB"CDEF"')

    def test_jsxAttributeValue(self):
        self.assertEqual(
            PSXAttributeInitializer.parse_strict('="img_cat.jpg"'), "img_cat.jpg"
        )
        self.assertRaises(ParseError, PSXAttributeInitializer.parse_strict, "src=")

    def test_jsx_Attribute(self):
        self.assertEqual(
            PSXAttribute.parse_strict("disabled"),
            PSXAttributeNode(PSXIdentiferNameNode("disabled"), None),
        )
        self.assertEqual(
            PSXAttribute.parse_strict("src='img_cat.jpg'"),
            PSXAttributeNode(
                PSXIdentiferNameNode("src"), PSXAttributeInitializerNode("img_cat.jpg")
            ),
        )
        self.assertEqual(
            PSXAttribute.parse_strict('src="img_cat.jpg"'),
            PSXAttributeNode(
                PSXIdentiferNameNode("src"), PSXAttributeInitializerNode("img_cat.jpg")
            ),
        )

    def test_jsx_selfClosingElement(self):
        self.assertEqual(PSXSelfClosingElement.parse("<component/>"), ("component", []))


class TextPixieDoc(unittest.TestCase):
    def test_jsxString(self):
        jsx = "<component></component>"
        self.assertEqual(
            JSXElement.parse(jsx),
            PSXBlockElementNode(PSXIdentiferNameNode("component"), [], []),
        )

        jsx_attr = "<component disabled></component>"
        self.assertEqual(
            JSXElement.parse(jsx_attr),
            PSXBlockElementNode(
                PSXIdentiferNameNode("component"),
                [PSXAttributeNode(PSXIdentiferNameNode("disabled"), None)],
                [],
            ),
        )

        jsx_attrval = "<component src='img_cat.jpg'></component>"
        self.assertEqual(
            JSXElement.parse(jsx_attrval),
            PSXBlockElementNode(
                PSXIdentiferNameNode("component"),
                [
                    PSXAttributeNode(
                        PSXIdentiferNameNode("src"),
                        PSXAttributeInitializerNode("img_cat.jpg"),
                    )
                ],
                [],
            ),
        )

        jsx_multiAttrval = "<component src='img_cat.jpg' width='300'></component>"
        self.assertEqual(
            JSXElement.parse(jsx_multiAttrval),
            PSXBlockElementNode(
                PSXIdentiferNameNode("component"),
                [
                    PSXAttributeNode(
                        PSXIdentiferNameNode("src"),
                        PSXAttributeInitializerNode("img_cat.jpg"),
                    ),
                    PSXAttributeNode(
                        PSXIdentiferNameNode("width"),
                        PSXAttributeInitializerNode("300"),
                    ),
                ],
                [],
            ),
        )

        jsx_multiAttrvalWithBooleanAttributes = (
            "<component src='img_cat.jpg' width='300' checked></component>"
        )
        self.assertEqual(
            JSXElement.parse(jsx_multiAttrvalWithBooleanAttributes),
            PSXBlockElementNode(
                PSXIdentiferNameNode("component"),
                [
                    PSXAttributeNode(
                        PSXIdentiferNameNode("src"),
                        PSXAttributeInitializerNode("img_cat.jpg"),
                    ),
                    PSXAttributeNode(
                        PSXIdentiferNameNode("width"),
                        PSXAttributeInitializerNode("300"),
                    ),
                    PSXAttributeNode(
                        PSXIdentiferNameNode("checked"),
                        None,
                    ),
                ],
                [],
            ),
        )

        jsx_unclosed = "<component>ABC"
        self.assertRaises(ParseError, JSXElement.parse_strict, (jsx_unclosed))

    def test_jsx_withChildren(self):
        jsx_children = "<component><nested></nested></component>"
        self.assertEqual(
            JSXElement.parse(jsx_children),
            PSXBlockElementNode(
                PSXIdentiferNameNode("component"),
                [],
                [PSXBlockElementNode(PSXIdentiferNameNode("nested"), [], [])],
            ),
        )

        jsx_childrenAndAttributes = (
            "<component disabled><nested width='300'></nested></component>"
        )
        self.assertEqual(
            JSXElement.parse(jsx_childrenAndAttributes),
            PSXBlockElementNode(
                PSXIdentiferNameNode("component"),
                [
                    PSXAttributeNode(
                        PSXIdentiferNameNode("disabled"),
                        None,
                    )
                ],
                [
                    PSXBlockElementNode(
                        PSXIdentiferNameNode("nested"),
                        [
                            PSXAttributeNode(
                                PSXIdentiferNameNode("width"),
                                PSXAttributeInitializerNode("300"),
                            )
                        ],
                        [],
                    )
                ],
            ),
        )


if __name__ == "__main__":
    unittest.main()
