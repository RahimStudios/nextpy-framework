"""
PSX AST Nodes - Pure Abstract Syntax Tree definitions
Structured representation for all PSX constructs
"""

from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import ast


class NodeType(Enum):
    """PSX node types"""
    ELEMENT = "element"
    TEXT = "text"
    EXPRESSION = "expression"
    LOGIC_BLOCK = "logic_block"
    COMPONENT = "component"
    FRAGMENT = "fragment"


class LogicType(Enum):
    """Logic block types"""
    IF = "if"
    FOR = "for"
    WHILE = "while"
    TRY = "try"


@dataclass
class PSXNode:
    """Base PSX AST node"""
    node_type: NodeType
    position: Optional[Tuple[int, int]] = None  # line, column for error reporting


@dataclass
class ElementNode(PSXNode):
    """HTML element node"""
    node_type: NodeType = NodeType.ELEMENT
    tag: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: Dict[str, str] = field(default_factory=dict)
    children: List['PSXNodeUnion'] = field(default_factory=list)
    key: Optional[str] = None
    self_closing: bool = False
    spread_props: List[str] = field(default_factory=list)


@dataclass
class TextNode(PSXNode):
    """Text content node"""
    node_type: NodeType = NodeType.TEXT
    content: str = ""


@dataclass
class ExpressionNode(PSXNode):
    """Expression node (e.g., {variable})"""
    node_type: NodeType = NodeType.EXPRESSION
    expression: str = ""
    parsed_expression: Optional[ast.AST] = None


@dataclass
class LogicNode(PSXNode):
    """Base logic block node"""
    node_type: NodeType = NodeType.LOGIC_BLOCK
    logic_type: LogicType = LogicType.IF
    body: List['PSXNodeUnion'] = field(default_factory=list)


@dataclass
class IfNode(LogicNode):
    """If/elif/else logic node"""
    node_type: NodeType = NodeType.LOGIC_BLOCK
    logic_type: LogicType = LogicType.IF
    condition: str = ""
    parsed_condition: Optional[ast.AST] = None
    then_body: List['PSXNodeUnion'] = field(default_factory=list)
    elif_conditions: List[str] = field(default_factory=list)
    elif_parsed_conditions: List[Optional[ast.AST]] = field(default_factory=list)
    elif_bodies: List[List['PSXNodeUnion']] = field(default_factory=list)
    else_body: Optional[List['PSXNodeUnion']] = None


@dataclass
class ForNode(LogicNode):
    """For loop logic node"""
    node_type: NodeType = NodeType.LOGIC_BLOCK
    logic_type: LogicType = LogicType.FOR
    variable: str = ""
    iterable: str = ""
    parsed_iterable: Optional[ast.AST] = None
    body: List['PSXNodeUnion'] = field(default_factory=list)


@dataclass
class WhileNode(LogicNode):
    """While loop logic node"""
    node_type: NodeType = NodeType.LOGIC_BLOCK
    logic_type: LogicType = LogicType.WHILE
    condition: str = ""
    parsed_condition: Optional[ast.AST] = None
    body: List['PSXNodeUnion'] = field(default_factory=list)


@dataclass
class TryNode(LogicNode):
    """Try/except/finally logic node"""
    node_type: NodeType = NodeType.LOGIC_BLOCK
    logic_type: LogicType = LogicType.TRY
    try_body: List['PSXNodeUnion'] = field(default_factory=list)
    except_var: Optional[str] = None
    except_body: Optional[List['PSXNodeUnion']] = None
    finally_body: Optional[List['PSXNodeUnion']] = None


@dataclass
class ComponentNode(PSXNode):
    """Component node"""
    node_type: NodeType = NodeType.COMPONENT
    name: str = ""
    props: Dict[str, Any] = field(default_factory=dict)
    events: Dict[str, str] = field(default_factory=dict)
    children: List['PSXNodeUnion'] = field(default_factory=list)
    key: Optional[str] = None
    spread_props: List[str] = field(default_factory=list)


@dataclass
class FragmentNode(PSXNode):
    """Fragment node (<>...</>)"""
    node_type: NodeType = NodeType.FRAGMENT
    children: List['PSXNodeUnion'] = field(default_factory=list)
    shorthand: bool = False


# Type aliases for better readability
PSXNodeUnion = Union[
    ElementNode,
    TextNode, 
    ExpressionNode,
    IfNode,
    ForNode,
    WhileNode,
    TryNode,
    ComponentNode,
    FragmentNode
]


class PSXASTParser:
    """Production-grade AST parser for PSX with safety and optimization"""
    
    @staticmethod
    def parse_expression(expression: str) -> Optional[ast.AST]:
        """Parse expression into AST with safety checks"""
        try:
            # Parse expression safely
            tree = ast.parse(expression, mode='eval')
            
            # Validate safety
            if PSXASTParser._is_safe_expression(tree):
                return tree.body
            else:
                return None
        except SyntaxError:
            return None
    
    @staticmethod
    def _is_safe_expression(node: ast.AST) -> bool:
        """Check if AST node is safe for evaluation"""
        allowed_nodes = {
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Compare, ast.BoolOp,
            ast.Num, ast.Str, ast.Name, ast.Load, ast.Constant,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
            ast.UAdd, ast.USub, ast.Not, ast.And, ast.Or,
            ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
            ast.Is, ast.IsNot, ast.In, ast.NotIn,
            ast.Call, ast.Attribute, ast.Subscript, ast.Index, ast.Slice,
            ast.List, ast.Tuple, ast.Dict
        }
        
        for child in ast.walk(node):
            if type(child) not in allowed_nodes:
                # Check for dangerous function calls
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):
                        func_name = child.func.id
                        if func_name in ['eval', 'exec', 'compile', '__import__', 'open', 'getattr', 'setattr', 'delattr']:
                            return False
                return False
        return True
    
    @staticmethod
    def evaluate_expression(parsed_ast: ast.AST, context: Dict[str, Any]) -> Any:
        """Safely evaluate parsed AST"""
        safe_context = {
            '__builtins__': {
                'len': len, 'str': str, 'int': int, 'float': float,
                'bool': bool, 'list': list, 'dict': dict, 'tuple': tuple,
                'range': range, 'enumerate': enumerate, 'zip': zip,
                'min': min, 'max': max, 'sum': sum, 'abs': abs,
                'round': round, 'sorted': sorted, 'reversed': reversed,
            },
            **context
        }
        
        try:
            return eval(compile(ast.Expression(parsed_ast), '<string>', 'eval'), safe_context)
        except Exception:
            return None


class PSXNodeValidator:
    """Production-grade node validation"""
    
    @staticmethod
    def validate_node(node: PSXNodeUnion) -> List[str]:
        """Validate PSX node and return errors"""
        errors = []
        
        if isinstance(node, ElementNode):
            errors.extend(PSXNodeValidator._validate_element(node))
        elif isinstance(node, ComponentNode):
            errors.extend(PSXNodeValidator._validate_component(node))
        elif isinstance(node, ExpressionNode):
            errors.extend(PSXNodeValidator._validate_expression(node))
        elif isinstance(node, (IfNode, ForNode, WhileNode, TryNode)):
            errors.extend(PSXNodeValidator._validate_logic(node))
        
        return errors
    
    @staticmethod
    def _validate_element(node: ElementNode) -> List[str]:
        """Validate element node"""
        errors = []
        
        # Check tag name
        if not node.tag:
            errors.append("Element tag cannot be empty")
        
        # Check self-closing consistency
        if node.self_closing and node.children:
            errors.append(f"Self-closing element <{node.tag}> cannot have children")
        
        # Check spread props
        for spread in node.spread_props:
            if not spread.startswith('...'):
                errors.append(f"Spread prop '{spread}' must start with '...'")
        
        return errors
    
    @staticmethod
    def _validate_component(node: ComponentNode) -> List[str]:
        """Validate component node"""
        errors = []
        
        # Check component name
        if not node.name:
            errors.append("Component name cannot be empty")
        elif not node.name[0].isupper():
            errors.append(f"Component name '{node.name}' should start with uppercase")
        
        return errors
    
    @staticmethod
    def _validate_expression(node: ExpressionNode) -> List[str]:
        """Validate expression node"""
        errors = []
        
        if not node.expression:
            errors.append("Expression cannot be empty")
        
        return errors
    
    @staticmethod
    def _validate_logic(node: Union[IfNode, ForNode, WhileNode, TryNode]) -> List[str]:
        """Validate logic node"""
        errors = []
        
        if isinstance(node, IfNode):
            if not node.condition:
                errors.append("If condition cannot be empty")
        elif isinstance(node, ForNode):
            if not node.variable or not node.iterable:
                errors.append("For loop requires variable and iterable")
        elif isinstance(node, WhileNode):
            if not node.condition:
                errors.append("While condition cannot be empty")
        
        return errors


class PSXNodeOptimizer:
    """Production-grade AST optimization"""
    
    @staticmethod
    def optimize_node(node: PSXNodeUnion) -> PSXNodeUnion:
        """Optimize PSX node for better performance"""
        if isinstance(node, ExpressionNode):
            return PSXNodeOptimizer._optimize_expression(node)
        elif isinstance(node, ElementNode):
            return PSXNodeOptimizer._optimize_element(node)
        else:
            return node
    
    @staticmethod
    def _optimize_expression(node: ExpressionNode) -> ExpressionNode:
        """Optimize expression node"""
        # Pre-parse expressions for better performance
        if node.expression and not node.parsed_expression:
            node.parsed_expression = PSXASTParser.parse_expression(node.expression)
        
        return node
    
    @staticmethod
    def _optimize_element(node: ElementNode) -> ElementNode:
        """Optimize element node"""
        # Optimize children recursively
        node.children = [PSXNodeOptimizer.optimize_node(child) for child in node.children]
        
        # Sort attributes for consistent rendering
        if node.attributes:
            node.attributes = dict(sorted(node.attributes.items()))
        
        return node


# Export all PSX AST components
__all__ = [
    # Core types
    'NodeType', 'LogicType', 'PSXNode', 'PSXNodeUnion',
    
    # Node types
    'ElementNode', 'TextNode', 'ExpressionNode', 'LogicNode',
    'IfNode', 'ForNode', 'WhileNode', 'TryNode',
    'ComponentNode', 'FragmentNode',
    
    # Production-grade utilities
    'PSXASTParser', 'PSXNodeValidator', 'PSXNodeOptimizer'
]
