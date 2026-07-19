"""
NextPy Plugin System Base Classes
Core plugin architecture and plugin management
"""

import os
import sys
import importlib.util
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class PluginPriority(Enum):
    """Plugin execution priority"""
    HIGHEST = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    LOWEST = 5


class PluginError(Exception):
    """Plugin-related errors"""
    pass


@dataclass
class PluginContext:
    """Context passed to plugins during transformation"""
    file_path: Path
    file_content: str
    metadata: Dict[str, Any]
    config: Dict[str, Any]
    debug: bool = False


@dataclass
class PluginResult:
    """Result of plugin transformation"""
    success: bool
    content: str
    metadata: Dict[str, Any]
    errors: List[str]
    warnings: List[str]


class JSXPlugin(ABC):
    """Base class for all JSX plugins"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.enabled = True
        self.priority = PluginPriority.NORMAL
        self.config = {}
        
    @abstractmethod
    def transform(self, context: PluginContext) -> PluginResult:
        """
        Transform JSX content
        
        Args:
            context: Plugin context with file info and content
            
        Returns:
            PluginResult with transformed content and metadata
        """
        pass
    
    def can_handle(self, context: PluginContext) -> bool:
        """
        Check if plugin can handle the given context
        
        Args:
            context: Plugin context
            
        Returns:
            True if plugin can handle this context
        """
        return True
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate plugin configuration
        
        Args:
            config: Plugin configuration
            
        Returns:
            True if configuration is valid
        """
        return True
    
    def get_dependencies(self) -> List[str]:
        """
        Get list of required dependencies
        
        Returns:
            List of dependency names
        """
        return []
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get plugin metadata
        
        Returns:
            Plugin metadata dictionary
        """
        return {
            "name": self.name,
            "version": self.version,
            "priority": self.priority.value,
            "enabled": self.enabled,
            "dependencies": self.get_dependencies()
        }


class PluginManager:
    """Manages plugin loading, execution, and lifecycle"""
    
    def __init__(self):
        self.plugins: List[JSXPlugin] = []
        self.plugin_registry: Dict[str, JSXPlugin] = {}
        self.hooks: Dict[str, List[Callable]] = {
            "before_transform": [],
            "after_transform": [],
            "on_error": [],
            "on_success": []
        }
        self.config: Dict[str, Any] = {}
        
    def register_plugin(self, plugin: JSXPlugin) -> None:
        """
        Register a plugin
        
        Args:
            plugin: Plugin instance to register
        """
        if plugin.name in self.plugin_registry:
            raise PluginError(f"Plugin '{plugin.name}' already registered")
        
        # Validate plugin
        if not plugin.validate_config(plugin.config):
            raise PluginError(f"Plugin '{plugin.name}' has invalid configuration")
        
        self.plugins.append(plugin)
        self.plugin_registry[plugin.name] = plugin
        
        # Sort plugins by priority
        self.plugins.sort(key=lambda p: p.priority.value)
    
    def unregister_plugin(self, name: str) -> None:
        """
        Unregister a plugin
        
        Args:
            name: Plugin name to unregister
        """
        if name not in self.plugin_registry:
            raise PluginError(f"Plugin '{name}' not found")
        
        plugin = self.plugin_registry[name]
        self.plugins.remove(plugin)
        del self.plugin_registry[name]
    
    def load_plugin_from_file(self, file_path: Path) -> JSXPlugin:
        """
        Load plugin from Python file
        
        Args:
            file_path: Path to plugin file
            
        Returns:
            Loaded plugin instance
        """
        if not file_path.exists():
            raise PluginError(f"Plugin file not found: {file_path}")
        
        try:
            spec = importlib.util.spec_from_file_location(
                file_path.stem, 
                file_path
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for plugin class
                plugin_class = getattr(module, "Plugin", None)
                if not plugin_class:
                    raise PluginError(f"No 'Plugin' class found in {file_path}")
                
                if not issubclass(plugin_class, JSXPlugin):
                    raise PluginError(f"Plugin class must inherit from JSXPlugin")
                
                return plugin_class()
                
        except Exception as e:
            raise PluginError(f"Failed to load plugin from {file_path}: {str(e)}")
    
    def load_plugins_from_directory(self, directory: Path) -> None:
        """
        Load all plugins from a directory
        
        Args:
            directory: Directory containing plugin files
        """
        if not directory.exists():
            return
        
        for file_path in directory.rglob("*.py"):
            if file_path.name.startswith("__"):
                continue
                
            try:
                plugin = self.load_plugin_from_file(file_path)
                self.register_plugin(plugin)
            except PluginError as e:
                print(f"Warning: Failed to load plugin {file_path}: {str(e)}")
    
    def transform_content(self, context: PluginContext) -> PluginResult:
        """
        Transform content using all registered plugins
        
        Args:
            context: Plugin context
            
        Returns:
            Final plugin result
        """
        result = PluginResult(
            success=True,
            content=context.file_content,
            metadata={},
            errors=[],
            warnings=[]
        )
        
        # Call before_transform hooks
        for hook in self.hooks["before_transform"]:
            try:
                hook(context)
            except Exception as e:
                result.errors.append(f"Hook error: {str(e)}")
        
        # Apply plugins in priority order
        for plugin in self.plugins:
            if not plugin.enabled:
                continue
                
            if not plugin.can_handle(context):
                continue
            
            try:
                # Update context for this plugin
                plugin_context = PluginContext(
                    file_path=context.file_path,
                    file_content=result.content,
                    metadata=result.metadata.copy(),
                    config=plugin.config,
                    debug=context.debug
                )
                
                plugin_result = plugin.transform(plugin_context)
                
                if not plugin_result.success:
                    result.errors.extend(plugin_result.errors)
                    # Call error hooks
                    for hook in self.hooks["on_error"]:
                        try:
                            hook(plugin, plugin_result)
                        except Exception:
                            pass
                else:
                    result.content = plugin_result.content
                    result.metadata.update(plugin_result.metadata)
                    result.warnings.extend(plugin_result.warnings)
                    
                    # Call success hooks
                    for hook in self.hooks["on_success"]:
                        try:
                            hook(plugin, plugin_result)
                        except Exception:
                            pass
                
            except Exception as e:
                error_msg = f"Plugin '{plugin.name}' failed: {str(e)}"
                result.errors.append(error_msg)
                
                # Call error hooks
                for hook in self.hooks["on_error"]:
                    try:
                        hook(plugin, e)
                    except Exception:
                        pass
        
        # Call after_transform hooks
        for hook in self.hooks["after_transform"]:
            try:
                hook(context, result)
            except Exception as e:
                result.errors.append(f"Hook error: {str(e)}")
        
        result.success = len(result.errors) == 0
        return result
    
    def add_hook(self, event: str, callback: Callable) -> None:
        """
        Add a hook for plugin events
        
        Args:
            event: Event name (before_transform, after_transform, on_error, on_success)
            callback: Callback function
        """
        if event not in self.hooks:
            raise PluginError(f"Unknown hook event: {event}")
        
        self.hooks[event].append(callback)
    
    def get_plugin_info(self) -> Dict[str, Any]:
        """
        Get information about all registered plugins
        
        Returns:
            Dictionary with plugin information
        """
        return {
            "total_plugins": len(self.plugins),
            "enabled_plugins": len([p for p in self.plugins if p.enabled]),
            "plugins": [plugin.get_metadata() for plugin in self.plugins]
        }
    
    def enable_plugin(self, name: str) -> None:
        """Enable a plugin"""
        if name not in self.plugin_registry:
            raise PluginError(f"Plugin '{name}' not found")
        
        self.plugin_registry[name].enabled = True
    
    def disable_plugin(self, name: str) -> None:
        """Disable a plugin"""
        if name not in self.plugin_registry:
            raise PluginError(f"Plugin '{name}' not found")
        
        self.plugin_registry[name].enabled = False
    
    def configure_plugin(self, name: str, config: Dict[str, Any]) -> None:
        """
        Configure a plugin
        
        Args:
            name: Plugin name
            config: Configuration dictionary
        """
        if name not in self.plugin_registry:
            raise PluginError(f"Plugin '{name}' not found")
        
        plugin = self.plugin_registry[name]
        
        if not plugin.validate_config(config):
            raise PluginError(f"Invalid configuration for plugin '{name}'")
        
        plugin.config.update(config)


# Global plugin manager instance
plugin_manager = PluginManager()
