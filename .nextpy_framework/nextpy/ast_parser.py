"""
NextPy AST Parser - Secure and reliable parsing using Abstract Syntax Trees
Replaces string-based evaluation with AST-based parsing for better security and performance
"""

import ast
import operator
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass


@dataclass
class ASTExpression:
    """Represents a parsed AST expression in NextPy Intermediate Representation"""
    type: str
    operator: Optional[str] = None
    left: Optional['ASTExpression'] = None
    right: Optional['ASTExpression'] = None
    value: Any = None
    name: Optional[str] = None
    args: Optional[List['ASTExpression']] = None
    body: Optional[List['ASTExpression']] = None


class ASTParser:
    """Converts Python AST to NextPy Intermediate Representation"""
    
    # Safe operators mapping
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
        ast.BitOr: operator.or_,
        ast.BitXor: operator.xor,
        ast.BitAnd: operator.and_,
        ast.MatMult: operator.matmul,
        
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.Is: operator.is_,
        ast.IsNot: operator.is_not,
        ast.In: lambda a, b: a in b,
        ast.NotIn: lambda a, b: a not in b,
        
        ast.And: lambda a, b: a and b,
        ast.Or: lambda a, b: a or b,
        ast.Not: operator.not_,
    }
    
    def __init__(self, allowed_names: Optional[Dict[str, Any]] = None):
        """
        Initialize AST parser with allowed names for security
        
        Args:
            allowed_names: Dictionary of allowed variable names and their values
        """
        self.allowed_names = allowed_names or {}
    
    def parse_expression(self, expression: str) -> ASTExpression:
        """
        Parse a Python expression into NextPy IR
        
        Args:
            expression: Python expression string
            
        Returns:
            ASTExpression in NextPy IR format
        """
        try:
            tree = ast.parse(expression, mode='eval')
            return self._convert_node(tree.body)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing expression: {e}")
    
    def parse_code(self, code: str) -> List[ASTExpression]:
        """
        Parse Python code into NextPy IR
        
        Args:
            code: Python code string
            
        Returns:
            List of ASTExpression in NextPy IR format
        """
        try:
            tree = ast.parse(code, mode='exec')
            return [self._convert_node(node) for node in tree.body]
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing code: {e}")
    
    def evaluate_expression(self, expression: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Safely evaluate a Python expression using AST
        
        Args:
            expression: Python expression string
            context: Additional context variables
            
        Returns:
            Evaluated result
        """
        ast_expr = self.parse_expression(expression)
        return self._evaluate_ast_expression(ast_expr, context)
    
    def _convert_node(self, node: ast.AST) -> ASTExpression:
        """Convert AST node to NextPy IR"""
        
        if isinstance(node, ast.Constant):
            return ASTExpression(
                type="Literal",
                value=node.value
            )
        
        elif isinstance(node, ast.Name):
            # Allow all names during parsing, check during evaluation
            return ASTExpression(
                type="Identifier",
                name=node.id
            )
        
        elif isinstance(node, ast.BinOp):
            return ASTExpression(
                type="BinaryExpression",
                operator=self._get_operator_name(node.op),
                left=self._convert_node(node.left),
                right=self._convert_node(node.right)
            )
        
        elif isinstance(node, ast.UnaryOp):
            return ASTExpression(
                type="UnaryExpression",
                operator=self._get_operator_name(node.op),
                left=self._convert_node(node.operand),
                right=None
            )
        
        elif isinstance(node, ast.BoolOp):
            return ASTExpression(
                type="LogicalExpression",
                operator=self._get_operator_name(node.op),
                left=self._convert_node(node.values[0]),
                right=self._convert_node(node.values[1]) if len(node.values) > 1 else None
            )
        
        elif isinstance(node, ast.Compare):
            if len(node.comparators) == 1:
                return ASTExpression(
                    type="BinaryExpression",
                    operator=self._get_operator_name(node.ops[0]),
                    left=self._convert_node(node.left),
                    right=self._convert_node(node.comparators[0])
                )
            else:
                # Handle chained comparisons (a < b < c)
                raise ValueError("Chained comparisons not yet supported")
        
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name not in self.allowed_names:
                    raise ValueError(f"Function '{func_name}' is not allowed")
                
                return ASTExpression(
                    type="CallExpression",
                    name=func_name,
                    args=[self._convert_node(arg) for arg in node.args]
                )
            else:
                raise ValueError("Only simple function calls are allowed")
        
        elif isinstance(node, ast.Attribute):
            return ASTExpression(
                type="MemberExpression",
                name=node.attr,
                left=self._convert_node(node.value)
            )
        
        elif isinstance(node, ast.List):
            return ASTExpression(
                type="ArrayExpression",
                args=[self._convert_node(elt) for elt in node.elts]
            )
        
        elif isinstance(node, ast.Dict):
            keys = [self._convert_node(key) for key in node.keys]
            values = [self._convert_node(value) for value in node.values]
            return ASTExpression(
                type="ObjectExpression",
                args=[keys, values]
            )
        
        else:
            raise ValueError(f"Unsupported AST node type: {type(node).__name__}")
    
    def _get_operator_name(self, op: ast.AST) -> str:
        """Get operator name from AST node"""
        operator_map = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
            ast.FloorDiv: "//",
            ast.Mod: "%",
            ast.Pow: "**",
            ast.LShift: "<<",
            ast.RShift: ">>",
            ast.BitOr: "|",
            ast.BitXor: "^",
            ast.BitAnd: "&",
            
            ast.Eq: "==",
            ast.NotEq: "!=",
            ast.Lt: "<",
            ast.LtE: "<=",
            ast.Gt: ">",
            ast.GtE: ">=",
            ast.Is: "is",
            ast.IsNot: "is not",
            ast.In: "in",
            ast.NotIn: "not in",
            
            ast.And: "and",
            ast.Or: "or",
            ast.Not: "not",
            
            ast.UAdd: "+",
            ast.USub: "-",
        }
        
        if type(op) in operator_map:
            return operator_map[type(op)]
        else:
            raise ValueError(f"Unsupported operator: {type(op).__name__}")
    
    def _evaluate_ast_expression(self, expr: ASTExpression, context: Optional[Dict[str, Any]] = None) -> Any:
        """Evaluate ASTExpression safely"""
        if context is None:
            context = {}
        
        # Merge allowed names with context
        eval_context = {**self.allowed_names, **context}
        
        if expr.type == "Literal":
            return expr.value
        
        elif expr.type == "Identifier":
            if expr.name in eval_context:
                return eval_context[expr.name]
            else:
                raise ValueError(f"Undefined variable: {expr.name}")
        
        elif expr.type == "BinaryExpression":
            left = self._evaluate_ast_expression(expr.left, context)
            right = self._evaluate_ast_expression(expr.right, context)
            
            op_func = self.OPERATORS.get(self._get_ast_operator(expr.operator))
            if op_func:
                return op_func(left, right)
            else:
                raise ValueError(f"Unsupported operator: {expr.operator}")
        
        elif expr.type == "UnaryExpression":
            operand = self._evaluate_ast_expression(expr.left, context)
            
            if expr.operator == "not":
                return not operand
            elif expr.operator == "-":
                return -operand
            elif expr.operator == "+":
                return +operand
            else:
                raise ValueError(f"Unsupported unary operator: {expr.operator}")
        
        elif expr.type == "LogicalExpression":
            left = self._evaluate_ast_expression(expr.left, context)
            
            if expr.operator == "and":
                # Short-circuit evaluation
                if not left:
                    return False
                right = self._evaluate_ast_expression(expr.right, context)
                return bool(right)
            elif expr.operator == "or":
                # Short-circuit evaluation
                if left:
                    return True
                right = self._evaluate_ast_expression(expr.right, context)
                return bool(right)
            else:
                raise ValueError(f"Unsupported logical operator: {expr.operator}")
        
        elif expr.type == "CallExpression":
            func = eval_context.get(expr.name)
            if not callable(func):
                raise ValueError(f"'{expr.name}' is not a function")
            
            args = [self._evaluate_ast_expression(arg, context) for arg in expr.args]
            return func(*args)
        
        elif expr.type == "ArrayExpression":
            return [self._evaluate_ast_expression(arg, context) for arg in expr.args]
        
        elif expr.type == "ObjectExpression":
            keys = expr.args[0]
            values = expr.args[1]
            result = {}
            for i, (key_expr, value_expr) in enumerate(zip(keys, values)):
                key = self._evaluate_ast_expression(key_expr, context)
                value = self._evaluate_ast_expression(value_expr, context)
                result[key] = value
            return result
        
        else:
            raise ValueError(f"Cannot evaluate expression type: {expr.type}")
    
    def _get_ast_operator(self, op_name: str) -> type:
        """Get AST operator class from operator name"""
        operator_map = {
            "+": ast.Add,
            "-": ast.Sub,
            "*": ast.Mult,
            "/": ast.Div,
            "//": ast.FloorDiv,
            "%": ast.Mod,
            "**": ast.Pow,
            "<<": ast.LShift,
            ">>": ast.RShift,
            "|": ast.BitOr,
            "^": ast.BitXor,
            "&": ast.BitAnd,
            
            "==": ast.Eq,
            "!=": ast.NotEq,
            "<": ast.Lt,
            "<=": ast.LtE,
            ">": ast.Gt,
            ">=": ast.GtE,
            "is": ast.Is,
            "is not": ast.IsNot,
            "in": ast.In,
            "not in": ast.NotIn,
        }
        
        return operator_map.get(op_name)


# Global AST parser instance with safe defaults
SAFE_PARSER = ASTParser(allowed_names={
    # Built-in functions
    'len': len,
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    'list': list,
    'dict': dict,
    'tuple': tuple,
    'set': set,
    'range': range,
    'enumerate': enumerate,
    'zip': zip,
    'map': map,
    'filter': filter,
    'sum': sum,
    'max': max,
    'min': min,
    'abs': abs,
    'round': round,
    'all': all,
    'any': any,
    
    # Math functions
    'math': __import__('math'),
    
    # Common constants
    'True': True,
    'False': False,
    'None': None,
})


def parse_expression_safe(expression: str, context: Optional[Dict[str, Any]] = None) -> Any:
    """
    Safely parse and evaluate a Python expression
    
    Args:
        expression: Python expression string
        context: Additional context variables
        
    Returns:
        Evaluated result
    """
    return SAFE_PARSER.evaluate_expression(expression, context)


def convert_to_ir(expression: str) -> Dict[str, Any]:
    """
    Convert Python expression to NextPy Intermediate Representation
    
    Args:
        expression: Python expression string
        
    Returns:
        Dictionary representation of ASTExpression
    """
    ast_expr = SAFE_PARSER.parse_expression(expression)
    
    def expr_to_dict(expr: ASTExpression) -> Dict[str, Any]:
        result = {
            'type': expr.type
        }
        
        if expr.operator is not None:
            result['operator'] = expr.operator
        if expr.value is not None:
            result['value'] = expr.value
        if expr.name is not None:
            result['name'] = expr.name
        if expr.left is not None:
            result['left'] = expr_to_dict(expr.left)
        if expr.right is not None:
            result['right'] = expr_to_dict(expr.right)
        if expr.args is not None:
            result['args'] = [expr_to_dict(arg) for arg in expr.args]
        if expr.body is not None:
            result['body'] = [expr_to_dict(node) for node in expr.body]
        
        return result
    
    return expr_to_dict(ast_expr)
