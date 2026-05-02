"""
NextPy PSX Runtime - Structured Action Execution Engine
Replacing JS string execution with structured action processing
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import json


@dataclass
class ComponentState:
    """Component state manager"""
    component_id: str
    state: Dict[str, Any]
    listeners: List[Callable]
    
    def __init__(self, component_id: str):
        self.component_id = component_id
        self.state = {}
        self.listeners = []
    
    def set(self, key: str, value: Any) -> None:
        """Set state value and notify listeners"""
        old_value = self.state.get(key)
        self.state[key] = value
        
        # Notify listeners
        for listener in self.listeners:
            try:
                listener(key, value, old_value)
            except Exception:
                pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get state value"""
        return self.state.get(key, default)
    
    def subscribe(self, listener: Callable) -> None:
        """Subscribe to state changes"""
        self.listeners.append(listener)


class ActionExecutor:
    """Structured action executor replacing JS string evaluation"""
    
    def __init__(self):
        self.components: Dict[str, ComponentState] = {}
        self.global_state: Dict[str, Any] = {}
        self.functions: Dict[str, Callable] = {}
        self._register_builtin_functions()
    
    def register_component(self, component_id: str) -> ComponentState:
        """Register a component state manager"""
        if component_id not in self.components:
            self.components[component_id] = ComponentState(component_id)
        return self.components[component_id]
    
    def execute_action(self, action: Dict[str, Any], component_id: Optional[str] = None) -> Any:
        """Execute a structured action"""
        action_type = action.get("type")
        data = action.get("data", {})
        
        try:
            if action_type == "SET_STATE":
                return self._execute_set_state(data, component_id)
            elif action_type == "GET_STATE":
                return self._execute_get_state(data, component_id)
            elif action_type == "CALL_FUNCTION":
                return self._execute_call_function(data)
            elif action_type == "BINARY_OP":
                return self._execute_binary_op(data)
            elif action_type == "UNARY_OP":
                return self._execute_unary_op(data)
            elif action_type == "COMPARE_OP":
                return self._execute_compare_op(data)
            elif action_type == "BOOLEAN_OP":
                return self._execute_boolean_op(data)
            elif action_type == "PRINT":
                return self._execute_print(data)
            elif action_type == "CONSTANT":
                return self._execute_constant(data)
            elif action_type == "VARIABLE":
                return self._execute_variable(data)
            elif action_type == "LIST":
                return self._execute_list(data)
            elif action_type == "DICT":
                return self._execute_dict(data)
            elif action_type == "INDEX":
                return self._execute_index(data)
            elif action_type == "ATTRIBUTE":
                return self._execute_attribute(data)
            else:
                return None
        except Exception as e:
            # Fallback for errors
            print(f"Action execution error: {e}")
            return None
    
    def _execute_set_state(self, data: Dict[str, Any], component_id: Optional[str] = None) -> None:
        """Execute SET_STATE action"""
        key = data.get("key")
        value = self._evaluate_expression(data.get("value"))
        
        if component_id and component_id in self.components:
            self.components[component_id].set(key, value)
        else:
            # Fallback to global state
            self.global_state[key] = value
    
    def _execute_get_state(self, data: Dict[str, Any], component_id: Optional[str] = None) -> Any:
        """Execute GET_STATE action"""
        key = data.get("key")
        
        if component_id and component_id in self.components:
            return self.components[component_id].get(key)
        else:
            return self.global_state.get(key)
    
    def _execute_call_function(self, data: Dict[str, Any]) -> Any:
        """Execute CALL_FUNCTION action"""
        func_name = data.get("function")
        args = [self._evaluate_expression(arg) for arg in data.get("args", [])]
        kwargs = {k: self._evaluate_expression(v) for k, v in data.get("kwargs", {}).items()}
        
        if func_name in self.functions:
            return self.functions[func_name](*args, **kwargs)
        else:
            # Try built-in functions
            builtin_functions = {
                "len": len,
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "list": list,
                "dict": dict,
                "range": range,
                "abs": abs,
                "min": min,
                "max": max,
                "sum": sum,
                "any": any,
                "all": all,
                "round": round,
            }
            
            if func_name in builtin_functions:
                return builtin_functions[func_name](*args, **kwargs)
            else:
                raise ValueError(f"Unknown function: {func_name}")
    
    def _execute_binary_op(self, data: Dict[str, Any]) -> Any:
        """Execute BINARY_OP action"""
        left = self._evaluate_expression(data.get("left"))
        right = self._evaluate_expression(data.get("right"))
        op = data.get("op")
        
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            return left / right
        elif op == "%":
            return left % right
        elif op == "**":
            return left ** right
        elif op == "//":
            return left // right
        elif op == "<<":
            return left << right
        elif op == ">>":
            return left >> right
        elif op == "|":
            return left | right
        elif op == "^":
            return left ^ right
        elif op == "&":
            return left & right
        else:
            raise ValueError(f"Unknown binary operator: {op}")
    
    def _execute_unary_op(self, data: Dict[str, Any]) -> Any:
        """Execute UNARY_OP action"""
        operand = self._evaluate_expression(data.get("operand"))
        op = data.get("op")
        
        if op == "+":
            return +operand
        elif op == "-":
            return -operand
        elif op == "not":
            return not operand
        elif op == "~":
            return ~operand
        else:
            raise ValueError(f"Unknown unary operator: {op}")
    
    def _execute_compare_op(self, data: Dict[str, Any]) -> bool:
        """Execute COMPARE_OP action"""
        left = self._evaluate_expression(data.get("left"))
        ops = data.get("ops", [])
        comparators = [self._evaluate_expression(c) for c in data.get("comparators", [])]
        
        result = True
        for i, (op, comparator) in enumerate(zip(ops, comparators)):
            if i == 0:
                if op == "==":
                    result = left == comparator
                elif op == "!=":
                    result = left != comparator
                elif op == "<":
                    result = left < comparator
                elif op == "<=":
                    result = left <= comparator
                elif op == ">":
                    result = left > comparator
                elif op == ">=":
                    result = left >= comparator
                elif op == "is":
                    result = left is comparator
                elif op == "is not":
                    result = left is not comparator
                elif op == "in":
                    result = left in comparator
                elif op == "not in":
                    result = left not in comparator
                else:
                    raise ValueError(f"Unknown comparison operator: {op}")
            else:
                # Chain comparisons (not fully implemented)
                pass
        
        return result
    
    def _execute_boolean_op(self, data: Dict[str, Any]) -> bool:
        """Execute BOOLEAN_OP action"""
        op = data.get("op")
        values = [self._evaluate_expression(v) for v in data.get("values", [])]
        
        if op == "and":
            return all(values)
        elif op == "or":
            return any(values)
        else:
            raise ValueError(f"Unknown boolean operator: {op}")
    
    def _execute_print(self, data: Dict[str, Any]) -> None:
        """Execute PRINT action"""
        args = [self._evaluate_expression(arg) for arg in data.get("args", [])]
        print(*args)
    
    def _execute_constant(self, data: Dict[str, Any]) -> Any:
        """Execute CONSTANT action"""
        return data.get("value")
    
    def _execute_variable(self, data: Dict[str, Any]) -> Any:
        """Execute VARIABLE action"""
        name = data.get("name")
        # Check component state first, then global state
        # This would need component_id context in real implementation
        return self.global_state.get(name)
    
    def _execute_list(self, data: Dict[str, Any]) -> List[Any]:
        """Execute LIST action"""
        elements = [self._evaluate_expression(elt) for elt in data.get("elements", [])]
        return elements
    
    def _execute_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute DICT action"""
        keys = data.get("keys", [])
        values = [self._evaluate_expression(v) for v in data.get("values", [])]
        
        result = {}
        for i, (key, value) in enumerate(zip(keys, values)):
            if key is not None:
                result[self._evaluate_expression(key)] = value
            else:
                # Handle **kwargs (not implemented)
                pass
        return result
    
    def _execute_index(self, data: Dict[str, Any]) -> Any:
        """Execute INDEX action"""
        value = self._evaluate_expression(data.get("value"))
        slice_val = self._evaluate_expression(data.get("slice"))
        
        return value[slice_val]
    
    def _execute_attribute(self, data: Dict[str, Any]) -> Any:
        """Execute ATTRIBUTE action"""
        obj = self._evaluate_expression(data.get("object"))
        attr = data.get("attr")
        
        return getattr(obj, attr)
    
    def _evaluate_expression(self, expr: Any) -> Any:
        """Evaluate a structured expression"""
        if expr is None:
            return None
        elif isinstance(expr, dict) and "type" in expr:
            return self.execute_action(expr)
        else:
            return expr
    
    def _register_builtin_functions(self) -> None:
        """Register built-in functions"""
        self.functions.update({
            "console_log": print,
            "alert": lambda msg: print(f"ALERT: {msg}"),
        })


# Global executor instance
action_executor = ActionExecutor()


def execute_actions(actions: List[Dict[str, Any]], component_id: Optional[str] = None) -> List[Any]:
    """Execute a list of structured actions"""
    results = []
    for action in actions:
        result = action_executor.execute_action(action, component_id)
        results.append(result)
    return results


def register_component_state(component_id: str) -> ComponentState:
    """Register a component and return its state manager"""
    return action_executor.register_component(component_id)
