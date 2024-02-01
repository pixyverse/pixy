from __future__ import annotations
from collections.abc import Generator
import re

from parsec import (
    generate,
    letter,
    many1,
    none_of,
    optional,
    regex,
    sepBy1,
    string,
    Parser,
)

from typing import Any, Callable


whitespace = regex(r"\s*", re.MULTILINE)
lexeme: Callable[[Parser[Any]], Parser[Any]] = lambda p: p << whitespace

lbracket: Parser[str] = lexeme(string("<"))
lclosedBracket: Parser[str] = lexeme(string("</"))
rbracket: Parser[str] = lexeme(string(">"))
rclosedBracket: Parser[str] = lexeme(string("/>"))

JSXIdentifier: Parser[str] = many1(letter()).parsecmap(lambda lst: "".join(lst))
JSXAttributeName: Parser[str] = JSXIdentifier


@generate
def JSXDoubleStringCharacters() -> Generator[Parser[str], str, str]:
    yield string('"')
    strchars = yield (many1(none_of('"'))).parsecmap(lambda lst: "".join(lst))
    yield string('"')
    return strchars


@generate
def JSXSingleStringCharacters() -> Generator[Parser[str], str, str]:
    yield string("'")
    strchars = yield many1(none_of("'")).parsecmap(lambda lst: "".join(lst))
    yield string("'")
    return strchars


JSXStringCharacters = JSXDoubleStringCharacters | JSXSingleStringCharacters
JSXAttributeValue = JSXStringCharacters
JSXAttributeInitializer: Parser[str] = string("=") >> JSXAttributeValue


@generate
def JSXAttribute():
    attrName = yield JSXAttributeName
    attrValues = yield optional(JSXAttributeInitializer)
    return (attrName, attrValues)


@generate
def JSXBlockElement():
    yield lbracket
    identifier = yield JSXIdentifier
    yield many1(whitespace)
    attributes = yield optional(sepBy1(JSXAttribute, whitespace))
    yield rbracket
    body = yield many1(optional(JSXElement))
    yield lclosedBracket
    yield string(identifier)
    yield rbracket
    return (identifier, body, attributes)


@generate
def JSXSelfClosingElement():
    yield lbracket
    identifier = yield JSXIdentifier
    yield many1(whitespace)
    attributes = yield optional(sepBy1(JSXAttribute, whitespace))
    yield many1(whitespace)
    yield rclosedBracket
    return (identifier, attributes)


JSXElement = JSXBlockElement | JSXSelfClosingElement
