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
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        import types

        module = types.ModuleType(module_name)
        module.__file__ = str(file_path)
        module.__original_file__ = str(file_path)

        if is_jsx_file(file_path):
            module.__is_jsx__ = True
            source = preprocess_content(original_content, str(file_path))
        else:
            # Plain Python (or .psx) module — spec_from_file_location can't
            # handle non-.py extensions, so exec the source directly.
            source = original_content

        # Compile against the original filename so tracebacks point at the
        # file the developer is editing (not a deleted temporary file).
        code = compile(source, str(file_path), "exec")
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

# ---------------------------------------------------------------------------
# Import hook — makes `import pages.components.card` work for files that use
# JSX `return (<div>…)` syntax, not just files loaded through load_jsx_module.
# Without this, importing a JSX component from another module raised
# SyntaxError because normal imports never ran the preprocessor.
# ---------------------------------------------------------------------------

_JSX_RETURN_RE = __import__('re').compile(r'return\s*\(?\s*<')


class _JSXModuleLoader:
    """Loader that preprocesses JSX before exec_module."""

    def __init__(self, origin, fallback_loader):
        self.origin = origin
        self.fallback_loader = fallback_loader

    def create_module(self, spec):
        if hasattr(self.fallback_loader, 'create_module'):
            return self.fallback_loader.create_module(spec)
        return None

    def get_source(self, fullname):
        try:
            return Path(self.origin).read_text(encoding='utf-8')
        except OSError:
            if hasattr(self.fallback_loader, 'get_source'):
                return self.fallback_loader.get_source(fullname)
            return None

    def get_code(self, fullname):
        source = self.get_source(fullname)
        if source is None:
            return None
        if _JSX_RETURN_RE.search(preprocess_masked_safe(source)):
            source = preprocess_content(source, self.origin)
        return compile(source, self.origin, 'exec')

    def exec_module(self, module):
        code = self.get_code(module.__name__)
        if code is not None:
            exec(code, module.__dict__)
            return
        if hasattr(self.fallback_loader, 'exec_module'):
            return self.fallback_loader.exec_module(module)


class _JSXImportFinder:
    """Meta path finder appended after the standard finders."""

    def find_spec(self, fullname, path=None, target=None):
        import importlib.machinery
        spec = importlib.machinery.PathFinder.find_spec(fullname, path, target)
        if spec is None or not spec.origin:
            return spec
        origin = spec.origin
        if not origin.endswith('.py'):
            return spec
        # Only project files — never site-packages or the framework itself
        try:
            origin_path = Path(origin).resolve()
            cwd = Path.cwd().resolve()
            if cwd not in origin_path.parents and origin_path != cwd:
                return spec
            if 'site-packages' in origin_path.parts:
                return spec
            # Framework runtime stays untouched; its test-suite files may
            # legitimately use JSX and are allowed through.
            if '.nextpy_framework' in origin_path.parts and 'tests' not in origin_path.parts:
                return spec
        except OSError:
            return spec
        try:
            head = origin_path.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            return spec
        if not _JSX_RETURN_RE.search(head):
            return spec
        spec.loader = _JSXModuleLoader(origin, spec.loader)
        return spec


def preprocess_masked_safe(source: str) -> str:
    """Cheap JSX check that ignores triple-quoted strings."""
    from .jsx_preprocessor import JSXPreprocessor
    return JSXPreprocessor._mask_strings(source)


def install_jsx_import_hook():
    """Install the JSX-aware import hook once.

    Inserted at the FRONT of sys.meta_path so it runs before the standard
    PathFinder — it delegates spec resolution to PathFinder itself and only
    swaps the loader for project .py files containing JSX returns.
    """
    if not any(isinstance(f, _JSXImportFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, _JSXImportFinder())


install_jsx_import_hook()
