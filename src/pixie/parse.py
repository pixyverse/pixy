import re
from parsec import *

whitespace = regex(r"\s*", re.MULTILINE)
lexeme = lambda p: p << whitespace

lbracket = lexeme(string("<"))
lclosedBracket = lexeme(string("</"))
rbracket = lexeme(string(">"))
rclosedBracket = lexeme(string("/>"))

JSXIdentifier = many1(letter()).parsecmap(lambda lst: "".join(lst))
JSXAttributeName = JSXIdentifier


@generate
def JSXDoubleStringCharacters():
    yield string('"')
    strchars = yield many1(none_of('"'))
    yield string('"')
    return "".join(strchars)


@generate
def JSXSingleStringCharacters():
    yield string("'")
    strchars = yield many1(none_of("'"))
    yield string("'")
    return "".join(strchars)


JSXStringCharacters = JSXDoubleStringCharacters | JSXSingleStringCharacters
JSXAttributeValue = JSXStringCharacters
JSXAttributeInitializer = string("=") >> JSXAttributeValue


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
