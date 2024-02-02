from __future__ import annotations
from collections.abc import Generator
import re

from parsec import (
    generate,
    letter,
    many,
    many1,
    none_of,
    optional,
    regex,
    sepBy1,
    string,
    Parser,
)

from typing import Any, Callable

from pixie.ast import (
    PSXAttributeInitializerNode,
    PSXAttributeNode,
    PSXBlockElementNode,
    PSXExpressionNode,
    PSXIdentiferNameNode,
)


whitespace = regex(r"\s*", re.MULTILINE)
lexeme: Callable[[Parser[Any]], Parser[Any]] = lambda p: p << whitespace

lbracket: Parser[str] = lexeme(string("<"))
lclosedBracket: Parser[str] = lexeme(string("</"))
rbracket: Parser[str] = lexeme(string(">"))
rclosedBracket: Parser[str] = lexeme(string("/>"))

PSXIdentifier: Parser[str] = many1(letter()).parsecmap(lambda lst: "".join(lst))
PSXAttributeName: Parser[str] = PSXIdentifier


@generate
def PSXDoubleStringCharacters() -> Generator[Parser[str], str, str]:
    yield string('"')
    strchars = yield (many1(none_of('"'))).parsecmap(lambda lst: "".join(lst))
    yield string('"')
    return strchars


@generate
def PSXSingleStringCharacters() -> Generator[Parser[str], str, str]:
    yield string("'")
    strchars = yield many1(none_of("'")).parsecmap(lambda lst: "".join(lst))
    yield string("'")
    return strchars


@generate
def PSXExpression():
    yield string("{")
    expr = yield PSXStringCharacters | many(none_of("}")).parsecmap(
        lambda lst: "".join(lst)
    )
    yield string("}")
    return PSXExpressionNode(expr)


PSXStringCharacters = PSXDoubleStringCharacters | PSXSingleStringCharacters
PSXAttributeValue = PSXStringCharacters | PSXExpression


@generate  # type: ignore[misc]
def PSXAttributeInitializer() -> Generator[Parser[str] | Parser[list[str]], Any, Any]:
    yield string("=")
    yield many(whitespace)
    attrValue = yield PSXAttributeValue
    return attrValue


@generate  # type: ignore[misc]
def PSXAttribute() -> (
    Generator[Parser[str] | Parser[str | None], Any, PSXAttributeNode]
):
    attrName = yield PSXAttributeName
    attrValue = yield optional(PSXAttributeInitializer)
    return PSXAttributeNode(
        PSXIdentiferNameNode(attrName),
        PSXAttributeInitializerNode(attrValue) if attrValue else None,
    )


@generate
def PSXBlockElement():
    yield lbracket
    identifier = yield PSXIdentifier
    yield many1(whitespace)
    attributes = yield optional(sepBy1(PSXAttribute, whitespace), [])
    yield rbracket
    body = yield many1(optional(JSXElement))
    yield lclosedBracket
    yield string(identifier)
    yield rbracket
    return PSXBlockElementNode(PSXIdentiferNameNode(identifier), attributes, body)


@generate
def PSXSelfClosingElement():
    yield lbracket
    identifier = yield PSXIdentifier
    yield many1(whitespace)
    attributes = yield optional(sepBy1(PSXAttribute, whitespace), [])
    yield many1(whitespace)
    yield rclosedBracket
    return (identifier, attributes)


JSXElement = PSXBlockElement | PSXSelfClosingElement
