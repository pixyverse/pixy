import unittest
from pixie.parse import *


class TestPixie(unittest.TestCase):
    def test_jsxIdentifier(self):
        self.assertEqual(JSXIdentifier.parse("abc"), "abc")
        self.assertRaises(ParseError, JSXIdentifier.parse_strict, "ab<")

    def test_jsxSelfClosingElement(self):
        self.assertEqual(JSXSelfClosingElement.parse("<hello/>"), ("hello", None))
        self.assertRaises(
            ParseError, JSXSelfClosingElement.parse, ["<hello", "<hello/>"]
        )

    def test_jsxStringCharacter(self):
        self.assertEqual(JSXStringCharacters.parse_strict('"a"'), "a")
        self.assertEqual(JSXStringCharacters.parse_strict('"abc"'), "abc")
        self.assertRaises(ParseError, JSXStringCharacters.parse_strict, '"AB"CDEF"')

    def test_jsxAttributeValue(self):
        self.assertEqual(
            JSXAttributeInitializer.parse_strict('="img_cat.jpg"'), "img_cat.jpg"
        )
        self.assertRaises(ParseError, JSXAttributeInitializer.parse_strict, "src=")

    def test_jsx_Attribute(self):
        self.assertEqual(JSXAttribute.parse_strict("disabled"), ("disabled", None))
        self.assertEqual(
            JSXAttribute.parse_strict("src='img_cat.jpg'"), ("src", "img_cat.jpg")
        )
        self.assertEqual(
            JSXAttribute.parse_strict('src="img_cat.jpg"'), ("src", "img_cat.jpg")
        )

    def test_jsx_selfClosingElement(self):
        self.assertEqual(
            JSXSelfClosingElement.parse("<component/>"), ("component", None)
        )


class TextPixieDoc(unittest.TestCase):
    def test_jsxString(self):
        jsx = "<component></component>"
        self.assertEqual(JSXElement.parse(jsx), ("component", [], None))

        jsx_attr = "<component disabled></component>"
        self.assertEqual(
            JSXElement.parse(jsx_attr), ("component", [], [("disabled", None)])
        )

        jsx_attrval = "<component src='img_cat.jpg'></component>"
        self.assertEqual(
            JSXElement.parse(jsx_attrval), ("component", [], [("src", "img_cat.jpg")])
        )

        jsx_multiAttrval = "<component src='img_cat.jpg' width='300'></component>"
        self.assertEqual(
            JSXElement.parse(jsx_multiAttrval),
            ("component", [], [("src", "img_cat.jpg"), ("width", "300")]),
        )

        jsx_multiAttrvalWithBooleanAttributes = (
            "<component src='img_cat.jpg' width='300' checked></component>"
        )
        self.assertEqual(
            JSXElement.parse(jsx_multiAttrvalWithBooleanAttributes),
            (
                "component",
                [],
                [("src", "img_cat.jpg"), ("width", "300"), ("checked", None)],
            ),
        )

        jsx_unclosed = "<component>ABC"
        self.assertRaises(ParseError, JSXElement.parse_strict, (jsx_unclosed))

    def test_jsx_withChildren(self):
        jsx_children = "<component><nested></nested></component>"
        self.assertEqual(
            JSXElement.parse(jsx_children), ("component", [("nested", [], None)], None)
        )


if __name__ == "__main__":
    unittest.main()
