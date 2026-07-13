"""
Compiler Introspection - Stable API for compilation information

Provides type-safe access to compiler configuration for the NextPy Agent.
This module wraps internal compiler implementation with a stable contract.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class CompilationTarget(Enum):
    """Stable compilation target enumeration"""
    PYTHON = "python"  # Server-side Python
    JAVASCRIPT = "javascript"  # Client-side JavaScript
    HTML = "html"  # Static HTML


class CompilationPhase(Enum):
    """Stable compilation phase enumeration"""
    PARSING = "parsing"
    AST_GENERATION = "ast_generation"
    OPTIMIZATION = "optimization"
    CODE_GENERATION = "code_generation"
    BUNDLING = "bundling"


@dataclass
class ClientEmitInfo:
    """Stable container for client emit information"""
    target: CompilationTarget
    runtime_version: str
    action_types: List[str] = field(default_factory=list)
    hydration_support: bool = True
    reactive_features: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        return {
            "target": self.target.value,
            "runtime_version": self.runtime_version,
            "action_types": self.action_types,
            "hydration_support": self.hydration_support,
            "reactive_features": self.reactive_features,
        }


@dataclass
class CompilationInfo:
    """Stable container for compilation information"""
    phases: List[CompilationPhase]
    server_target: CompilationTarget
    client_target: CompilationTarget
    optimizations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        return {
            "phases": [phase.value for phase in self.phases],
            "server_target": self.server_target.value,
            "client_target": self.client_target.value,
            "optimizations": self.optimizations,
        }


def get_compilation_target() -> CompilationInfo:
    """
    Get compilation target information.
    
    This function provides a stable interface for the agent to understand
    how NextPy compiles PSX to executable code.
    
    Returns:
        CompilationInfo with stable structure
    """
    return CompilationInfo(
        phases=[
            CompilationPhase.PARSING,
            CompilationPhase.AST_GENERATION,
            CompilationPhase.OPTIMIZATION,
            CompilationPhase.CODE_GENERATION,
        ],
        server_target=CompilationTarget.PYTHON,
        client_target=CompilationTarget.JAVASCRIPT,  # Based on architectural decision
        optimizations=[
            "dead_code_elimination",
            "constant_folding",
            "expression_caching",
            "attribute_sorting",
            "tree_shaking",
        ],
    )


def get_client_emit_info() -> ClientEmitInfo:
    """
    Get client emit information.
    
    Returns information about how NextPy emits client-side code,
    including the JavaScript runtime and action system.
    
    Returns:
        ClientEmitInfo with stable structure
    """
    return ClientEmitInfo(
        target=CompilationTarget.JAVASCRIPT,  # Based on architectural decision
        runtime_version="1.0.0",
        action_types=[
            "SET_STATE",
            "SET_STATE_BATCH",
            "GET_STATE",
            "CALL_FUNCTION",
            "CALL_METHOD",
            "BINARY_OP",
            "UNARY_OP",
            "COMPARE_OP",
            "BOOLEAN_OP",
            "PRINT",
            "CONSTANT",
            "VARIABLE",
            "LIST",
            "DICT",
            "INDEX",
            "ATTRIBUTE",
        ],
        hydration_support=True,
        reactive_features=[
            "state_management",
            "component_lifecycle",
            "event_handling",
            "conditional_rendering",
            "list_rendering",
            "data_binding",
            "hooks_system",
        ],
    )


__all__ = [
    "CompilationTarget",
    "CompilationPhase",
    "ClientEmitInfo",
    "CompilationInfo",
    "get_compilation_target",
    "get_client_emit_info",
]
