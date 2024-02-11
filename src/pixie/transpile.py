from types import CodeType
from typing import Any, assert_never, List
from pixie.ast import (
    PSXAttributeNode,
    PSXBlockElementNode,
    JSXRootNode,
    PSXExpressionNode,
    PSXSelfClosingElementNode,
)
import ast


def compileEx(expr, bindings) -> CodeType:
    exprCode = ast.parse(expr, "", "eval")
    compiled = compile(exprCode, "", "eval")
    return eval(compiled, bindings)


def transpileAttributes(attributes: List[PSXAttributeNode], bindings) -> str:
    attrStr = ""
    if len(attributes) > 0:
        attrStr = " "
        for attr in attributes:
            attrValue = None
            if attr.attributeInitializer is not None:
                match attr.attributeInitializer.value:
                    case PSXExpressionNode(expr):
                        attrValue = (
                            f"{attr.attributeName.name}='{compileEx(expr, bindings)}'"
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

            def createSelfClosingElement(bindings: dict[str, Any] | None = None):
                return f"<{iNode.name}{transpileAttributes(attribs, bindings)}/>"

            return createSelfClosingElement
        case PSXBlockElementNode(iNode, attribs, children):
            print(f"Block Element Node {iNode}")
            name = iNode.name

            def createBlockElement(bindings: dict[str, Any] | None = None):
                attrStr = transpileAttributes(attribs, bindings)
                nested = [transpile(child) for child in children]
                return f"<{name}{attrStr}>{''.join(f() for f in nested)}</{name}>"

            return createBlockElement

        case _ as unreachable:
            assert_never(unreachable)
