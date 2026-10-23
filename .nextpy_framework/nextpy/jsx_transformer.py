"""
JSX Transformer - Runtime transformation of JSX syntax in Python files
"""

import os
import sys
import tempfile
import importlib.util
from pathlib import Path
from typing import Any, Dict, Optional
from .jsx_preprocessor import preprocess_content, is_jsx_file


class JSXTransformer:
    """Transform Python files with JSX syntax at import time"""
    
    def __init__(self):
        self.transformed_modules = {}
    
    def load_jsx_module(self, file_path: Path, module_name: str = None):
        """Load a Python module with JSX syntax"""
        if module_name is None:
            module_name = file_path.stem
        
        # Check if file contains JSX
        if not is_jsx_file(file_path):
            # Regular Python file - load normally
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        
        # Transform JSX syntax
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        transformed_content = preprocess_content(original_content)
        
        # Compile against the original filename so tracebacks point at the
        # file the developer is editing (not a deleted temporary file).
        import types

        module = types.ModuleType(module_name)
        module.__file__ = str(file_path)
        module.__original_file__ = str(file_path)
        module.__is_jsx__ = True

        code = compile(transformed_content, str(file_path), "exec")
        exec(code, module.__dict__)

        sys.modules[module_name] = module
        return module
    
    def reload_jsx_module(self, file_path: Path, module_name: str = None):
        """Reload a JSX module"""
        if module_name is None:
            module_name = file_path.stem
        
        # Remove from cache if exists
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        return self.load_jsx_module(file_path, module_name)


# Global transformer instance
transformer = JSXTransformer()


def load_jsx_module(file_path: Path, module_name: str = None):
    """Convenience function to load JSX module"""
    return transformer.load_jsx_module(file_path, module_name)


def reload_jsx_module(file_path: Path, module_name: str = None):
    """Convenience function to reload JSX module"""
    return transformer.reload_jsx_module(file_path, module_name)