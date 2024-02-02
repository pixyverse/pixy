from typing import assert_never, List
from pixie.ast import (
    PSXAttributeNode,
    PSXBlockElementNode,
    JSXRootNode,
    PSXExpressionNode,
    PSXSelfClosingElementNode,
)
import ast


def evalExpression(expr):
    exprCode = ast.parse(expr, "", "eval")
    compiled = compile(exprCode, "", "eval")
    return eval(compiled)


def transpileAttributes(attributes: List[PSXAttributeNode]) -> str:
    attrStr = ""
    if len(attributes) > 0:
        attrStr = " "
        for attr in attributes:
            attrValue = None
            if attr.attributeInitializer is not None:
                match attr.attributeInitializer.value:
                    case PSXExpressionNode(expr):
                        attrValue = (
                            f"{attr.attributeName.name}='{evalExpression(expr)}'"
                        )
                    case str(strVal):
                        attrValue = f"{attr.attributeName.name}='{strVal}'"
                    case _ as unreachable:
                        assert_never(unreachable)
            else:
                attrValue = f"{attr.attributeName.name}"
            attrStr += attrValue
    return attrStr


def transpile(ast: JSXRootNode):
    match ast:
        case PSXSelfClosingElementNode(iNode, attribs):
            print(f"Self Closing Node: {iNode}")

            def createSelfClosingElement():
                return f"<{iNode.name}{transpileAttributes(attribs)}/>"

            return createSelfClosingElement
        case PSXBlockElementNode(iNode, attribs, children):
            print(f"Block Element Node {iNode}")
            name = iNode.name

            def createBlockElement():
                attrStr = transpileAttributes(attribs)
                nested = map(transpile, children)
                return f"<{name}{attrStr}>{''.join(f() for f in nested)}</{name}>"

            return createBlockElement

        case _ as unreachable:
            assert_never(unreachable)
