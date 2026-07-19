"""
Plugin Configuration Management
Handles plugin configuration loading and management
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .base import PluginManager, PluginError


@dataclass
class PluginConfig:
    """Plugin configuration structure"""
    name: str
    enabled: bool = True
    config: Dict[str, Any] = None
    priority: Optional[int] = None
    dependencies: List[str] = None


class PluginConfigManager:
    """Manages plugin configuration files and loading"""
    
    def __init__(self, config_file: Optional[Path] = None):
        self.config_file = config_file or Path("nextpy-plugins.json")
        self.configs: Dict[str, PluginConfig] = {}
        
    def load_config(self) -> Dict[str, PluginConfig]:
        """Load plugin configuration from file"""
        if not self.config_file.exists():
            self.configs = self._get_default_config()
            return self.configs
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.configs = {}
            for name, config_data in data.items():
                self.configs[name] = PluginConfig(
                    name=name,
                    enabled=config_data.get('enabled', True),
                    config=config_data.get('config', {}),
                    priority=config_data.get('priority'),
                    dependencies=config_data.get('dependencies', [])
                )
                
            return self.configs
            
        except Exception as e:
            raise PluginError(f"Failed to load plugin config: {str(e)}")
    
    def save_config(self) -> None:
        """Save plugin configuration to file"""
        try:
            config_data = {}
            for name, config in self.configs.items():
                config_data[name] = {
                    'enabled': config.enabled,
                    'config': config.config,
                    'priority': config.priority,
                    'dependencies': config.dependencies
                }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2)
                
        except Exception as e:
            raise PluginError(f"Failed to save plugin config: {str(e)}")
    
    def add_plugin_config(self, config: PluginConfig) -> None:
        """Add or update a plugin configuration"""
        self.configs[config.name] = config
    
    def remove_plugin_config(self, name: str) -> None:
        """Remove a plugin configuration"""
        if name in self.configs:
            del self.configs[name]
    
    def get_plugin_config(self, name: str) -> Optional[PluginConfig]:
        """Get configuration for a specific plugin"""
        return self.configs.get(name)
    
    def _get_default_config(self) -> Dict[str, PluginConfig]:
        """Get default plugin configuration"""
        default_plugins = [
            PluginConfig("validation", True, {}, 1),
            PluginConfig("tailwind", True, {}, 2),
            PluginConfig("typescript", True, {}, 3),
            PluginConfig("style", True, {}, 4),
            PluginConfig("component", True, {}, 5)
        ]
        
        return {plugin.name: plugin for plugin in default_plugins}
    
    def configure_plugins(self, plugin_manager: PluginManager) -> None:
        """Configure plugins based on configuration"""
        for name, config in self.configs.items():
            try:
                if not config.enabled:
                    plugin_manager.disable_plugin(name)
                    continue
                
                if config.config:
                    plugin_manager.configure_plugin(name, config.config)
                    
                if config.priority:
                    # Update plugin priority
                    plugin = plugin_manager.plugin_registry.get(name)
                    if plugin:
                        from .base import PluginPriority
                        plugin.priority = PluginPriority(config.priority)
                        # Re-sort plugins
                        plugin_manager.plugins.sort(key=lambda p: p.priority.value)
                        
            except Exception as e:
                print(f"Warning: Failed to configure plugin '{name}': {str(e)}")


def setup_default_plugins(plugin_manager: PluginManager) -> None:
    """Setup default plugins for the plugin manager"""
    from .builtin import (
        ValidationPlugin,
        TailwindPlugin,
        TypeScriptPlugin,
        StylePlugin,
        ComponentPlugin
    )
    
    default_plugins = [
        ValidationPlugin(),
        TailwindPlugin(),
        TypeScriptPlugin(),
        StylePlugin(),
        ComponentPlugin()
    ]
    
    for plugin in default_plugins:
        try:
            plugin_manager.register_plugin(plugin)
        except PluginError as e:
            print(f"Warning: Failed to register plugin '{plugin.name}': {str(e)}")
