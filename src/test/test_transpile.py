import unittest

from pixie.ast import (
    PSXAttributeInitializerNode,
    PSXAttributeNode,
    PSXBlockElementNode,
    PSXExpressionNode,
    PSXIdentiferNameNode,
    PSXSelfClosingElementNode,
)
from pixie.transpile import transpile


class TestTranspile(unittest.TestCase):
    def test_transpileSelf(self) -> None:
        node = PSXSelfClosingElementNode(PSXIdentiferNameNode("component"), [])
        tree = transpile(node)
        self.assertEqual(tree(), "<component/>")

    def test_transpileSelfWithAttributes(self) -> None:
        attribute: PSXAttributeNode = PSXAttributeNode(PSXIdentiferNameNode("disabled"))
        node = PSXSelfClosingElementNode(PSXIdentiferNameNode("component"), [attribute])
        tree = transpile(node)
        self.assertEqual(tree(), "<component disabled/>")

    def test_transpileBlockElement(self) -> None:
        node = PSXBlockElementNode(PSXIdentiferNameNode("component"), [], [])
        tree = transpile(node)
        self.assertEqual(tree(), "<component></component>")

    def test_transpileBlockElementWithAttributes(self) -> None:
        node = PSXBlockElementNode(PSXIdentiferNameNode("component"), [], [])
        tree = transpile(node)
        self.assertEqual(tree(), "<component></component>")

    def test_transpileNestedBlockElements(self) -> None:
        childNode = PSXBlockElementNode(PSXIdentiferNameNode("nested"), [], [])
        node = PSXBlockElementNode(PSXIdentiferNameNode("component"), [], [childNode])
        tree = transpile(node)
        self.assertEqual(tree(), "<component><nested></nested></component>")

    def test_transpileNestedBlockElementsWithAttributes(self) -> None:
        attribute1: PSXAttributeNode = PSXAttributeNode(
            PSXIdentiferNameNode("disabled")
        )
        attribute2: PSXAttributeNode = PSXAttributeNode(
            PSXIdentiferNameNode("width"), PSXAttributeInitializerNode("300")
        )
        childNode = PSXBlockElementNode(
            PSXIdentiferNameNode("nested"), [attribute1], []
        )
        node = PSXBlockElementNode(
            PSXIdentiferNameNode("component"), [attribute2], [childNode]
        )
        tree = transpile(node)
        self.assertEqual(
            tree(), "<component width='300'><nested disabled></nested></component>"
        )

    def test_transpileAttributeExpressions(self) -> None:
        attribute: PSXAttributeNode = PSXAttributeNode(
            PSXIdentiferNameNode("width"),
            PSXAttributeInitializerNode(PSXExpressionNode("1+1")),
        )
        node = PSXSelfClosingElementNode(PSXIdentiferNameNode("component"), [attribute])
        tree = transpile(node)
        self.assertEqual(tree(), "<component width='2'/>")

    def test_transpileAttributeExpressionsWithVars(self) -> None:
        attribute: PSXAttributeNode = PSXAttributeNode(
            PSXIdentiferNameNode("width"),
            PSXAttributeInitializerNode(PSXExpressionNode("1+a")),
        )
        node = PSXSelfClosingElementNode(PSXIdentiferNameNode("component"), [attribute])
        tree = transpile(node)
        self.assertEqual(tree({"a": 1}), "<component width='2'/>")

    def test_transpileAttributeExpressionsWithFormattedString(self) -> None:
        attribute: PSXAttributeNode = PSXAttributeNode(
            PSXIdentiferNameNode("display"),
            PSXAttributeInitializerNode(PSXExpressionNode("f'1+a={1+a}'")),
        )
        node = PSXSelfClosingElementNode(PSXIdentiferNameNode("component"), [attribute])
        tree = transpile(node)
        self.assertEqual(tree({"a": 1}), "<component display='1+a=2'/>")


if __name__ == "__main__":
    unittest.main()
