"""
AST Introspection - Stable API for inspecting PSX AST nodes

Provides type-safe access to PSX AST structure for the NextPy Agent.
This module wraps the internal PSX AST implementation with a stable contract.
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class ASTNodeType(Enum):
    """Stable AST node type enumeration"""
    ELEMENT = "element"
    TEXT = "text"
    EXPRESSION = "expression"
    LOGIC_BLOCK = "logic_block"
    COMPONENT = "component"
    FRAGMENT = "fragment"


class LogicBlockType(Enum):
    """Stable logic block type enumeration"""
    IF = "if"
    FOR = "for"
    WHILE = "while"
    TRY = "try"


@dataclass
class ASTNodeInfo:
    """Stable container for AST node information"""
    node_type: ASTNodeType
    tag: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    children: List['ASTNodeInfo'] = field(default_factory=list)
    expression: Optional[str] = None
    logic_type: Optional[LogicBlockType] = None
    component_name: Optional[str] = None
    props: Dict[str, Any] = field(default_factory=dict)
    position: Optional[tuple] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        return {
            "node_type": self.node_type.value,
            "tag": self.tag,
            "attributes": self.attributes,
            "children": [child.to_dict() for child in self.children],
            "expression": self.expression,
            "logic_type": self.logic_type.value if self.logic_type else None,
            "component_name": self.component_name,
            "props": self.props,
            "position": self.position,
        }


def get_ast_info(node: Any) -> ASTNodeInfo:
    """
    Extract stable AST information from a PSX AST node.
    
    This function provides a stable interface that abstracts away internal
    PSX implementation details. The agent should only use this function
    to inspect AST nodes.
    
    Args:
        node: A PSX AST node (ElementNode, TextNode, etc.)
        
    Returns:
        ASTNodeInfo with stable structure
    """
    from nextpy.psx.core.ast_nodes import (
        PSXNodeUnion, ElementNode, TextNode, ExpressionNode,
        ComponentNode, FragmentNode, IfNode, ForNode, WhileNode, TryNode,
        NodeType, LogicType,
    )
    
    if isinstance(node, ElementNode):
        return ASTNodeInfo(
            node_type=ASTNodeType.ELEMENT,
            tag=node.tag,
            attributes=node.attributes,
            children=[get_ast_info(child) for child in node.children],
            position=node.position,
        )
    elif isinstance(node, TextNode):
        return ASTNodeInfo(
            node_type=ASTNodeType.TEXT,
            expression=node.content,
            position=node.position,
        )
    elif isinstance(node, ExpressionNode):
        return ASTNodeInfo(
            node_type=ASTNodeType.EXPRESSION,
            expression=node.expression,
            position=node.position,
        )
    elif isinstance(node, ComponentNode):
        return ASTNodeInfo(
            node_type=ASTNodeType.COMPONENT,
            component_name=node.name,
            props=node.props,
            attributes=node.events,  # Events stored in attributes for introspection
            children=[get_ast_info(child) for child in node.children],
            position=node.position,
        )
    elif isinstance(node, FragmentNode):
        return ASTNodeInfo(
            node_type=ASTNodeType.FRAGMENT,
            children=[get_ast_info(child) for child in node.children],
            position=node.position,
        )
    elif isinstance(node, IfNode):
        return ASTNodeInfo(
            node_type=ASTNodeType.LOGIC_BLOCK,
            logic_type=LogicBlockType.IF,
            expression=node.condition,
            children=[get_ast_info(child) for child in node.then_body],
            position=node.position,
        )
    elif isinstance(node, ForNode):
        return ASTNodeInfo(
            node_type=ASTNodeType.LOGIC_BLOCK,
            logic_type=LogicBlockType.FOR,
            expression=node.iterable,
            attributes={"variable": node.variable},
            children=[get_ast_info(child) for child in node.body],
            position=node.position,
        )
    elif isinstance(node, WhileNode):
        return ASTNodeInfo(
            node_type=ASTNodeType.LOGIC_BLOCK,
            logic_type=LogicBlockType.WHILE,
            expression=node.condition,
            children=[get_ast_info(child) for child in node.body],
            position=node.position,
        )
    elif isinstance(node, TryNode):
        return ASTNodeInfo(
            node_type=ASTNodeType.LOGIC_BLOCK,
            logic_type=LogicBlockType.TRY,
            children=[get_ast_info(child) for child in node.try_body],
            position=node.position,
        )
    else:
        # Fallback for unknown node types
        return ASTNodeInfo(
            node_type=ASTNodeType.TEXT,
            expression=str(node),
        )


def get_node_type(node: Any) -> ASTNodeType:
    """Get the stable node type for a PSX AST node"""
    info = get_ast_info(node)
    return info.node_type


def get_node_children(node: Any) -> List[ASTNodeInfo]:
    """Get children of a PSX AST node as stable info objects"""
    info = get_ast_info(node)
    return info.children


def get_node_attributes(node: Any) -> Dict[str, Any]:
    """Get attributes of a PSX AST node"""
    info = get_ast_info(node)
    return info.attributes


__all__ = [
    "ASTNodeType",
    "LogicBlockType", 
    "ASTNodeInfo",
    "get_ast_info",
    "get_node_type",
    "get_node_children",
    "get_node_attributes",
]
