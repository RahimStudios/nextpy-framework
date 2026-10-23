"""
NextPy Plugin System
Extensible plugin architecture for JSX transformers and custom processors
"""

from .base import JSXPlugin, PluginManager, PluginError, plugin_manager
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
    'plugin_manager',
    'TailwindPlugin',
    'TypeScriptPlugin',
    'StylePlugin',
    'ComponentPlugin',
    'ValidationPlugin'
]
