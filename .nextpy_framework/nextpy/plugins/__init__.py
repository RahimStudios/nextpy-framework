"""
NextPy Plugin System
Extensible plugin architecture for JSX transformers and custom processors
"""

from .base import JSXPlugin, PluginManager, PluginError
from .builtin import (
    TailwindPlugin,
    TypeScriptPlugin,
    StylePlugin,
    ComponentPlugin,
    ValidationPlugin
)

__all__ = [
    'JSXPlugin',
    'PluginManager', 
    'PluginError',
    'TailwindPlugin',
    'TypeScriptPlugin',
    'StylePlugin',
    'ComponentPlugin',
    'ValidationPlugin'
]
