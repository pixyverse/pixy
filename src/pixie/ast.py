from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class PSXIdentiferNameNode:
    name: str


@dataclass
class PSXAttributeInitializerNode:
    value: str


@dataclass
class PSXAttributeNode:
    attributeName: PSXIdentiferNameNode
    attributeInitializer: Optional[PSXAttributeInitializerNode] = None


@dataclass
class PSXSelfClosingElementNode:
    identifierName: PSXIdentiferNameNode
    attributes: List[PSXAttributeNode]


@dataclass
class PSXBlockElementNode:
    identifierName: PSXIdentiferNameNode
    attributes: List[PSXAttributeNode]
    children: List[JSXRootNode]


JSXRootNode = PSXSelfClosingElementNode | PSXBlockElementNode
