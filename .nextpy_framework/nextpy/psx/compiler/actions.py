"""
NextPy PSX Compiler - Structured Actions System
Replacing regex-based compilation with AST-based action generation
"""

import ast
from typing import Dict, List, Any, Union, Optional
from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    """Structured action types"""
    SET_STATE = "SET_STATE"
    GET_STATE = "GET_STATE"
    CALL_FUNCTION = "CALL_FUNCTION"
    BINARY_OP = "BINARY_OP"
    UNARY_OP = "UNARY_OP"
    COMPARE_OP = "COMPARE_OP"
    BOOLEAN_OP = "BOOLEAN_OP"
    CONDITIONAL = "CONDITIONAL"
    LAMBDA = "LAMBDA"
    RETURN = "RETURN"
    PRINT = "PRINT"
    LIST = "LIST"
    DICT = "DICT"
    INDEX = "INDEX"
    ATTRIBUTE = "ATTRIBUTE"
    CONSTANT = "CONSTANT"
    VARIABLE = "VARIABLE"


@dataclass
class Action:
    """Structured action representation"""
    type: ActionType
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert action to dictionary for JSON serialization"""
        result = {
            'type': self.type.value,
            'data': self._serialize_data(self.data)
        }
        if self.metadata:
            result['metadata'] = self.metadata
        return result
    
    def _serialize_data(self, data: Any) -> Any:
        """Recursively serialize data to JSON-compatible format"""
        if isinstance(data, Action):
            return data.to_dict()
        elif isinstance(data, dict):
            return {k: self._serialize_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._serialize_data(item) for item in data]
        elif isinstance(data, ActionType):
            return data.value
        else:
            return data


class ActionCompiler:
    """AST-based action compiler replacing regex-based compilation"""
    
    def __init__(self):
        self.current_scope = {}
        self.handler_context = {}
    
    def compile_handler(self, handler_code: str, handler_name: str) -> List[Action]:
        """Compile handler code to structured actions"""
        import ast
        
        try:
            # Handle lambda expressions by wrapping them
            if handler_code.strip().startswith('lambda'):
                # Wrap lambda in a function call to make it valid Python
                wrapped_code = f"({handler_code})"
                tree = ast.parse(wrapped_code, mode='eval')
                if isinstance(tree.body, ast.Lambda):
                    # Compile the lambda body directly
                    action = self._compile_expression(tree.body.body)
                    if action:
                        return [action]
            else:
                # Regular function code
                tree = ast.parse(handler_code)
                actions = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                        action = self._compile_expression(node.value)
                        if action:
                            actions.append(action)
                    elif isinstance(node, ast.Assign):
                        # Handle variable assignments
                        action = self._compile_assignment(node)
                        if action:
                            actions.append(action)
                    elif isinstance(node, ast.Return):
                        # Handle return statements
                        action = self._compile_return(node)
                        if action:
                            actions.append(action)
                
                return actions
            
            return []
            
        except SyntaxError as e:
            # Fallback for syntax errors
            return [Action(
                type=ActionType.PRINT,
                data={"message": f"Handler compilation error: {e}"},
                metadata={"error": True}
            )]
    
    def _compile_expression(self, node: ast.AST) -> Optional[Action]:
        """Compile AST expression to action"""
        if isinstance(node, ast.Call):
            return self._compile_call(node)
        elif isinstance(node, ast.BinOp):
            return self._compile_binary_op(node)
        elif isinstance(node, ast.UnaryOp):
            return self._compile_unary_op(node)
        elif isinstance(node, ast.Compare):
            return self._compile_compare_op(node)
        elif isinstance(node, ast.BoolOp):
            return self._compile_boolean_op(node)
        elif isinstance(node, ast.Name):
            return self._compile_variable(node)
        elif isinstance(node, ast.Constant):
            return self._compile_constant(node)
        elif isinstance(node, ast.List):
            return self._compile_list(node)
        elif isinstance(node, ast.Dict):
            return self._compile_dict(node)
        elif isinstance(node, ast.Subscript):
            return self._compile_index(node)
        elif isinstance(node, ast.Attribute):
            return self._compile_attribute(node)
        elif isinstance(node, ast.Lambda):
            return self._compile_lambda(node)
        
        return None
    
    def _compile_call(self, node: ast.Call) -> Action:
        """Compile function call to action"""
        func_name = self._get_function_name(node.func)
        args = [self._compile_expression(arg) for arg in node.args]
        kwargs = {kw.arg: self._compile_expression(kw.value) for kw in node.keywords if kw.arg}
        
        # Special handling for common functions
        if func_name == 'setCount':
            return Action(
                type=ActionType.SET_STATE,
                data={
                    "key": "count",
                    "value": args[0] if args else {"type": "CONSTANT", "data": {"value": None}}
                }
            )
        elif func_name == 'setName':
            return Action(
                type=ActionType.SET_STATE,
                data={
                    "key": "name", 
                    "value": args[0] if args else {"type": "CONSTANT", "data": {"value": None}}
                }
            )
        elif func_name == 'setLoading':
            return Action(
                type=ActionType.SET_STATE,
                data={
                    "key": "loading",
                    "value": args[0] if args else {"type": "CONSTANT", "data": {"value": None}}
                }
            )
        elif func_name == 'print':
            return Action(
                type=ActionType.PRINT,
                data={
                    "args": args
                }
            )
        else:
            return Action(
                type=ActionType.CALL_FUNCTION,
                data={
                    "function": func_name,
                    "args": args,
                    "kwargs": kwargs
                }
            )
    
    def _compile_binary_op(self, node: ast.BinOp) -> Action:
        """Compile binary operation to action"""
        left = self._compile_expression(node.left)
        right = self._compile_expression(node.right)
        
        op_map = {
            ast.Add: "+",
            ast.Sub: "-", 
            ast.Mult: "*",
            ast.Div: "/",
            ast.Mod: "%",
            ast.Pow: "**",
            ast.LShift: "<<",
            ast.RShift: ">>",
            ast.BitOr: "|",
            ast.BitXor: "^",
            ast.BitAnd: "&",
            ast.FloorDiv: "//"
        }
        
        op = op_map.get(type(node.op), "+")
        
        return Action(
            type=ActionType.BINARY_OP,
            data={
                "left": left.to_dict() if left else None,
                "op": op,
                "right": right.to_dict() if right else None
            }
        )
    
    def _compile_unary_op(self, node: ast.UnaryOp) -> Action:
        """Compile unary operation to action"""
        operand = self._compile_expression(node.operand)
        
        op_map = {
            ast.UAdd: "+",
            ast.USub: "-",
            ast.Not: "not",
            ast.Invert: "~"
        }
        
        op = op_map.get(type(node.op), "-")
        
        return Action(
            type=ActionType.UNARY_OP,
            data={
                "op": op,
                "operand": operand.to_dict() if operand else None
            }
        )
    
    def _compile_compare_op(self, node: ast.Compare) -> Action:
        """Compile comparison operation to action"""
        left = self._compile_expression(node.left)
        ops = []
        comparators = []
        
        for op, comparator in zip(node.ops, node.comparators):
            op_map = {
                ast.Eq: "==",
                ast.NotEq: "!=",
                ast.Lt: "<",
                ast.LtE: "<=",
                ast.Gt: ">",
                ast.GtE: ">=",
                ast.Is: "is",
                ast.IsNot: "is not",
                ast.In: "in",
                ast.NotIn: "not in"
            }
            
            ops.append(op_map.get(type(op), "=="))
            comparators.append(self._compile_expression(comparator))
        
        return Action(
            type=ActionType.COMPARE_OP,
            data={
                "left": left.to_dict() if left else None,
                "ops": ops,
                "comparators": [c.to_dict() if c else None for c in comparators]
            }
        )
    
    def _compile_boolean_op(self, node: ast.BoolOp) -> Action:
        """Compile boolean operation to action"""
        values = [self._compile_expression(value) for value in node.values]
        
        op_map = {
            ast.And: "and",
            ast.Or: "or"
        }
        
        op = op_map.get(type(node.op), "and")
        
        return Action(
            type=ActionType.BOOLEAN_OP,
            data={
                "op": op,
                "values": [v.to_dict() if v else None for v in values]
            }
        )
    
    def _compile_variable(self, node: ast.Name) -> Action:
        """Compile variable reference to action"""
        return Action(
            type=ActionType.VARIABLE,
            data={
                "name": node.id
            }
        )
    
    def _compile_constant(self, node: ast.Constant) -> Action:
        """Compile constant to action"""
        return Action(
            type=ActionType.CONSTANT,
            data={
                "value": node.value,
                "type": type(node.value).__name__
            }
        )
    
    def _compile_list(self, node: ast.List) -> Action:
        """Compile list to action"""
        elements = [self._compile_expression(elt) for elt in node.elts]
        
        return Action(
            type=ActionType.LIST,
            data={
                "elements": [e.to_dict() if e else None for e in elements]
            }
        )
    
    def _compile_dict(self, node: ast.Dict) -> Action:
        """Compile dictionary to action"""
        keys = []
        values = []
        
        for key, value in zip(node.keys, node.values):
            if key is not None:
                keys.append(self._compile_expression(key))
            else:
                keys.append(None)  # **kwargs
            values.append(self._compile_expression(value))
        
        return Action(
            type=ActionType.DICT,
            data={
                "keys": [k.to_dict() if k else None for k in keys],
                "values": [v.to_dict() if v else None for v in values]
            }
        )
    
    def _compile_index(self, node: ast.Subscript) -> Action:
        """Compile index operation to action"""
        value = self._compile_expression(node.value)
        slice_val = self._compile_expression(node.slice)
        
        return Action(
            type=ActionType.INDEX,
            data={
                "value": value.to_dict() if value else None,
                "slice": slice_val.to_dict() if slice_val else None
            }
        )
    
    def _compile_attribute(self, node: ast.Attribute) -> Action:
        """Compile attribute access to action"""
        value = self._compile_expression(node.value)
        
        return Action(
            type=ActionType.ATTRIBUTE,
            data={
                "object": value.to_dict() if value else None,
                "attr": node.attr
            }
        )
    
    def _compile_lambda(self, node: ast.Lambda) -> Action:
        """Compile lambda to action"""
        args = [arg.arg for arg in node.args.args]
        body = self._compile_expression(node.body)
        
        return Action(
            type=ActionType.LAMBDA,
            data={
                "args": args,
                "body": body.to_dict() if body else None
            }
        )
    
    def _compile_assignment(self, node: ast.Assign) -> Optional[Action]:
        """Compile assignment to action"""
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            return None
        
        target_name = node.targets[0].id
        value = self._compile_expression(node.value)
        
        return Action(
            type=ActionType.SET_STATE,
            data={
                "key": target_name,
                "value": value.to_dict() if value else None
            }
        )
    
    def _compile_return(self, node: ast.Return) -> Optional[Action]:
        """Compile return statement to action"""
        value = self._compile_expression(node.value) if node.value else None
        
        return Action(
            type=ActionType.RETURN,
            data={
                "value": value.to_dict() if value else None
            }
        )
    
    def _get_function_name(self, node: ast.AST) -> str:
        """Extract function name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_function_name(node.value)}.{node.attr}"
        else:
            return "unknown"


# Global compiler instance
action_compiler = ActionCompiler()


def compile_handler_to_actions(handler_code: str, handler_name: str) -> List[Dict[str, Any]]:
    """Compile handler code to structured actions (main entry point)"""
    actions = action_compiler.compile_handler(handler_code, handler_name)
    return [action.to_dict() for action in actions]
