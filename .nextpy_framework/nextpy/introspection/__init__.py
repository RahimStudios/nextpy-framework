"""
NextPy Introspection Module - Stable Agent Contract

This module provides a stable, versioned API for the NextPy Agent to inspect
and understand NextPy framework internals. This is the ONLY module the agent
is allowed to depend on from the framework.

Version: 1.0.0
Stability: Stable (semantic versioning applies)
"""

__version__ = "1.0.0"
__api_version__ = "1.0"

# Core introspection APIs
from nextpy.introspection.ast import (
    get_ast_info,
    get_node_type,
    get_node_children,
    get_node_attributes,
    ASTNodeInfo,
)

from nextpy.introspection.components import (
    get_component_info,
    get_component_props,
    get_component_hooks,
    ComponentInfo,
)

from nextpy.introspection.framework import (
    get_framework_info,
    get_parser_info,
    get_runtime_info,
    FrameworkInfo,
)

from nextpy.introspection.compiler import (
    get_compilation_target,
    get_client_emit_info,
    CompilationTarget,
)

__all__ = [
    # Version info
    "__version__",
    "__api_version__",
    
    # AST introspection
    "get_ast_info",
    "get_node_type", 
    "get_node_children",
    "get_node_attributes",
    "ASTNodeInfo",
    
    # Component introspection
    "get_component_info",
    "get_component_props",
    "get_component_hooks",
    "ComponentInfo",
    
    # Framework introspection
    "get_framework_info",
    "get_parser_info",
    "get_runtime_info",
    "FrameworkInfo",
    
    # Compiler introspection
    "get_compilation_target",
    "get_client_emit_info",
    "CompilationTarget",
]
