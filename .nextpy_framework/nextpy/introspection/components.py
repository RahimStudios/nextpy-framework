"""
Component Introspection - Stable API for inspecting PSX components

Provides type-safe access to component metadata for the NextPy Agent.
This module wraps internal component implementation with a stable contract.
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class ComponentType(Enum):
    """Stable component type enumeration"""
    FUNCTIONAL = "functional"
    CLASS_BASED = "class_based"
    HOOKS_BASED = "hooks_based"


class HookType(Enum):
    """Stable hook type enumeration"""
    STATE = "useState"
    EFFECT = "useEffect"
    REDUCER = "useReducer"
    CONTEXT = "useContext"
    REF = "useRef"
    MEMO = "useMemo"
    CALLBACK = "useCallback"
    CUSTOM = "custom"


@dataclass
class HookInfo:
    """Stable container for hook information"""
    hook_type: HookType
    hook_name: str
    dependencies: Optional[List[str]] = None
    initial_value: Any = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        return {
            "hook_type": self.hook_type.value,
            "hook_name": self.hook_name,
            "dependencies": self.dependencies,
            "initial_value": str(self.initial_value) if self.initial_value is not None else None,
        }


@dataclass
class ComponentInfo:
    """Stable container for component information"""
    name: str
    component_type: ComponentType
    props: Dict[str, Any] = field(default_factory=dict)
    hooks: List[HookInfo] = field(default_factory=list)
    children: List[str] = field(default_factory=list)
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        return {
            "name": self.name,
            "component_type": self.component_type.value,
            "props": self.props,
            "hooks": [hook.to_dict() for hook in self.hooks],
            "children": self.children,
            "file_path": self.file_path,
            "line_number": self.line_number,
        }


def get_component_info(component_func: Callable) -> ComponentInfo:
    """
    Extract stable component information from a PSX component function.
    
    This function provides a stable interface that abstracts away internal
    PSX component implementation details.
    
    Args:
        component_func: A PSX component function
        
    Returns:
        ComponentInfo with stable structure
    """
    import inspect
    
    # Basic component information
    name = component_func.__name__ if hasattr(component_func, '__name__') else "Anonymous"
    component_type = ComponentType.FUNCTIONAL  # Default assumption
    
    # Try to get source information
    file_path = None
    line_number = None
    try:
        file_path = inspect.getfile(component_func)
        line_number = inspect.getsourcelines(component_func)[1]
    except (TypeError, OSError):
        pass
    
    # Extract props from function signature
    props = {}
    try:
        sig = inspect.signature(component_func)
        for param_name, param in sig.parameters.items():
            if param_name != 'self':  # Skip self for class components
                props[param_name] = {
                    "default": str(param.default) if param.default != inspect.Parameter.empty else None,
                    "annotation": str(param.annotation) if param.annotation != inspect.Parameter.empty else None,
                }
    except (ValueError, TypeError):
        pass
    
    # Extract hooks by analyzing source code
    hooks = _extract_hooks_from_function(component_func)
    
    return ComponentInfo(
        name=name,
        component_type=component_type,
        props=props,
        hooks=hooks,
        file_path=file_path,
        line_number=line_number,
    )


def get_component_props(component_func: Callable) -> Dict[str, Any]:
    """Get props schema for a component"""
    info = get_component_info(component_func)
    return info.props


def get_component_hooks(component_func: Callable) -> List[HookInfo]:
    """Get hooks used by a component"""
    info = get_component_info(component_func)
    return info.hooks


def _extract_hooks_from_function(component_func: Callable) -> List[HookInfo]:
    """
    Extract hook information from component function source.
    
    This is a simplified implementation that analyzes the source code
    to identify hook calls. A production version would use AST analysis.
    """
    import inspect
    import re
    
    hooks = []
    
    try:
        source = inspect.getsource(component_func)
        
        # Common hook patterns
        hook_patterns = {
            HookType.STATE: r'useState\s*\(',
            HookType.EFFECT: r'useEffect\s*\(',
            HookType.REDUCER: r'useReducer\s*\(',
            HookType.CONTEXT: r'useContext\s*\(',
            HookType.REF: r'useRef\s*\(',
            HookType.MEMO: r'useMemo\s*\(',
            HookType.CALLBACK: r'useCallback\s*\(',
        }
        
        for hook_type, pattern in hook_patterns.items():
            matches = re.findall(pattern, source)
            for _ in matches:
                hooks.append(HookInfo(
                    hook_type=hook_type,
                    hook_name=hook_type.value,
                ))
        
        # Detect custom hooks (functions starting with 'use')
        custom_hook_pattern = r'use\w+\s*\('
        custom_matches = re.findall(custom_hook_pattern, source)
        for match in custom_matches:
            hook_name = match.strip('(')
            if hook_name not in [h.hook_name for h in hooks]:
                hooks.append(HookInfo(
                    hook_type=HookType.CUSTOM,
                    hook_name=hook_name,
                ))
                
    except (OSError, TypeError):
        pass
    
    return hooks


__all__ = [
    "ComponentType",
    "HookType",
    "HookInfo",
    "ComponentInfo",
    "get_component_info",
    "get_component_props",
    "get_component_hooks",
]
