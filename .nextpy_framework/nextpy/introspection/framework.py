"""
Framework Introspection - Stable API for framework metadata

Provides type-safe access to framework information for the NextPy Agent.
This module wraps internal framework implementation with a stable contract.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class ParserType(Enum):
    """Stable parser type enumeration"""
    PSX = "psx"
    JSX = "jsx"
    LEGACY = "legacy"


class RuntimeType(Enum):
    """Stable runtime type enumeration"""
    SERVER = "server"
    CLIENT = "client"
    HYBRID = "hybrid"


@dataclass
class ParserInfo:
    """Stable container for parser information"""
    parser_type: ParserType
    version: str
    features: List[str] = field(default_factory=list)
    supported_syntax: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        return {
            "parser_type": self.parser_type.value,
            "version": self.version,
            "features": self.features,
            "supported_syntax": self.supported_syntax,
        }


@dataclass
class RuntimeInfo:
    """Stable container for runtime information"""
    runtime_type: RuntimeType
    version: str
    features: List[str] = field(default_factory=list)
    client_target: str = "javascript"  # Based on our JS vs WASM decision
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        return {
            "runtime_type": self.runtime_type.value,
            "version": self.version,
            "features": self.features,
            "client_target": self.client_target,
        }


@dataclass
class FrameworkInfo:
    """Stable container for framework information"""
    name: str
    version: str
    description: str
    parser: ParserInfo
    runtime: RuntimeInfo
    features: List[str] = field(default_factory=list)
    capabilities: Dict[str, bool] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "parser": self.parser.to_dict(),
            "runtime": self.runtime.to_dict(),
            "features": self.features,
            "capabilities": self.capabilities,
        }


def get_framework_info() -> FrameworkInfo:
    """
    Get comprehensive framework information.
    
    This function provides a stable interface for the agent to understand
    the NextPy framework's capabilities and configuration.
    
    Returns:
        FrameworkInfo with stable structure
    """
    import nextpy
    
    return FrameworkInfo(
        name="NextPy",
        version=nextpy.__version__,
        description="The Python Web Framework with file-based routing, SSR, SSG, and PSX",
        parser=get_parser_info(),
        runtime=get_runtime_info(),
        features=[
            "file-based routing",
            "server-side rendering (SSR)",
            "static site generation (SSG)",
            "PSX (Python Syntax Extension)",
            "React-style hooks",
            "component system",
            "API routes",
            "database integration",
            "authentication",
        ],
        capabilities={
            "ssr": True,
            "ssg": True,
            "csr": True,
            "api_routes": True,
            "database": True,
            "auth": True,
            "websockets": True,
            "static_files": True,
            "hot_reload": True,
            "typescript_support": False,  # Python-first framework
        },
    )


def get_parser_info() -> ParserInfo:
    """
    Get parser information.
    
    Returns information about the PSX parser implementation.
    
    Returns:
        ParserInfo with stable structure
    """
    return ParserInfo(
        parser_type=ParserType.PSX,
        version="1.0.0",
        features=[
            "recursive-descent parsing",
            "thread-safe",
            "cross-platform",
            "AST-based",
            "safe expression evaluation",
            "component support",
            "logic blocks (if/for/while/try)",
        ],
        supported_syntax=[
            "HTML elements",
            "PSX components",
            "expressions {expr}",
            "fragments <>...</>",
            "logic blocks {if}...{/if}",
            "loops {for}...{/for}",
            "spread props {...props}",
            "event handlers onClick",
        ],
    )


def get_runtime_info() -> RuntimeInfo:
    """
    Get runtime information.
    
    Returns information about the NextPy runtime implementation.
    
    Returns:
        RuntimeInfo with stable structure
    """
    return RuntimeInfo(
        runtime_type=RuntimeType.HYBRID,
        version="1.0.0",
        features=[
            "server-side rendering",
            "client-side hydration",
            "reactive state management",
            "JavaScript action runtime",
            "component lifecycle",
            "hooks system",
            "event handling",
        ],
        client_target="javascript",  # Based on architectural decision
    )


__all__ = [
    "ParserType",
    "RuntimeType",
    "ParserInfo",
    "RuntimeInfo",
    "FrameworkInfo",
    "get_framework_info",
    "get_parser_info",
    "get_runtime_info",
]
