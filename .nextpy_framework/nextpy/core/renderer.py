"""
NextPy Renderer - Server-side rendering with PSX and Jinja2
Handles PSX components, templates, layouts, and routing with complete PSX integration
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, List
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
from markupsafe import Markup

# Import PSX for complete integration
sys.path.insert(0, str(Path(__file__).parent.parent))
from nextpy.psx import (
    compile_psx, render_psx, psx, PSXElement, PSXParser,
    component, useState, useEffect, process_python_logic,
    VNode, create_element, render, update, get_vdom_metrics
)

from nextpy.components.head import Head
from nextpy.components.link import Link


class Renderer:
    """
    Enhanced server-side renderer using PSX and Jinja2
    Supports PSX components, layouts, templates, and complete component composition
    """
    
    def __init__(
        self, 
        templates_dir: str = "templates",
        pages_dir: str = "pages",
        public_dir: str = "public"
    ):
        self.templates_dir = Path(templates_dir)
        self.pages_dir = Path(pages_dir)
        self.public_dir = Path(public_dir)
        
        loader = FileSystemLoader([
            str(self.templates_dir),
            str(self.pages_dir),
        ])
        
        self.env = Environment(
            loader=loader,
            autoescape=select_autoescape(["html", "xml"]),
            enable_async=True,
        )
        
        # PSX integration
        self.psx_parser = PSXParser()
        self.component_cache = {}  # Cache for compiled PSX components
        self.vdom_cache = {}  # Cache for Virtual DOM nodes
        
        self._register_globals()
        self._register_filters()
        self._register_psx_functions()
        
    def _register_psx_functions(self) -> None:
        """Register PSX functions as Jinja2 globals"""
        self.env.globals.update({
            # PSX Core Functions
            'psx': psx,
            'render_psx': render_psx,
            'component': component,
            
            # PSX Hooks
            'useState': useState,
            'useEffect': useEffect,
            'process_python_logic': process_python_logic,
            
            # Virtual DOM Functions
            'create_element': create_element,
            'render': render,
            'update': update,
            'get_vdom_metrics': get_vdom_metrics,
            
            # PSX Utilities
            'map_list': self._safe_import('nextpy.psx.map_list'),
            'filter_list': self._safe_import('nextpy.psx.filter_list'),
            'conditional': self._safe_import('nextpy.psx.conditional'),
            'class_names': self._safe_import('nextpy.psx.class_names'),
            'style_props': self._safe_import('nextpy.psx.style_props'),
        })
    
    def _safe_import(self, module_path: str, attr_name: str = None):
        """Safely import PSX utilities"""
        try:
            if attr_name:
                module = __import__(module_path, fromlist=[attr_name])
                return getattr(module, attr_name)
            else:
                return __import__(module_path)
        except ImportError:
            return lambda *args, **kwargs: ""
    
    def _register_globals(self) -> None:
        """Register global functions and components available in templates"""
        self.env.globals["Head"] = Head
        self.env.globals["Link"] = Link
        self.env.globals["Markup"] = Markup
        self.env.globals["Renderer"] = self  # Allow templates to access renderer
        
        self.env.globals["range"] = range
        self.env.globals["len"] = len
        self.env.globals["str"] = str
        self.env.globals["int"] = int
        self.env.globals["list"] = list
        self.env.globals["dict"] = dict
        self.env.globals["enumerate"] = enumerate
        
    def _register_filters(self) -> None:
        """Register custom Jinja2 filters"""
        self.env.filters["json"] = self._json_filter
        self.env.filters["date"] = self._date_filter
        self.env.filters["truncate_words"] = self._truncate_words_filter
        
    @staticmethod
    def _json_filter(value: Any) -> str:
        """Convert value to JSON string"""
        import json
        return json.dumps(value)
        
    @staticmethod
    def _date_filter(value: Any, format_str: str = "%Y-%m-%d") -> str:
        """Format a date value"""
        from datetime import datetime
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        if hasattr(value, "strftime"):
            return value.strftime(format_str)
        return str(value)
        
    @staticmethod
    def _truncate_words_filter(value: str, num_words: int = 20) -> str:
        """Truncate text to a number of words"""
        words = value.split()
        if len(words) <= num_words:
            return value
        return " ".join(words[:num_words]) + "..."
        
    def render(
        self,
        template_name: str,
        context: Optional[Dict[str, Any]] = None,
        layout: Optional[str] = None,
    ) -> str:
        """
        Render a template with the given context
        
        Args:
            template_name: Name of the template file
            context: Dictionary of variables to pass to template
            layout: Optional layout template to wrap the content
            
        Returns:
            Rendered HTML string
        """
        context = context or {}
        
        context.setdefault("__page__", template_name)
        context.setdefault("__layout__", layout)
        
        try:
            template = self.env.get_template(template_name)
        except TemplateNotFound:
            template_path = self._find_template(template_name)
            if template_path:
                template = self.env.get_template(str(template_path))
            else:
                raise
                
        content = template.render(**context)
        
        if layout:
            try:
                layout_template = self.env.get_template(layout)
                content = layout_template.render(content=Markup(content), **context)
            except TemplateNotFound:
                pass
                
        return content
        
    async def render_async(
        self,
        template_name: str,
        context: Optional[Dict[str, Any]] = None,
        layout: Optional[str] = None,
    ) -> str:
        """Async version of render"""
        context = context or {}
        
        context.setdefault("__page__", template_name)
        context.setdefault("__layout__", layout)
        
        try:
            template = self.env.get_template(template_name)
        except TemplateNotFound:
            template_path = self._find_template(template_name)
            if template_path:
                template = self.env.get_template(str(template_path))
            else:
                raise
                
        content = await template.render_async(**context)
        
        if layout:
            try:
                layout_template = self.env.get_template(layout)
                content = await layout_template.render_async(
                    content=Markup(content), 
                    **context
                )
            except TemplateNotFound:
                pass
                
        return content
        
    def _find_template(self, template_name: str) -> Optional[Path]:
        """Find a template by searching in multiple locations"""
        search_paths = [
            self.templates_dir / template_name,
            self.templates_dir / f"{template_name}.html",
            self.templates_dir / f"{template_name}.jinja2",
        ]
        
        for path in search_paths:
            if path.exists():
                return path.relative_to(self.templates_dir)
                
        return None
        
    def render_component(
        self, 
        component_func: callable,
        props: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Enhanced component renderer with full PSX support
        Components can be:
        1. Python functions returning HTML strings
        2. PSX components using @component decorator
        3. PSX elements created with psx()
        4. Virtual DOM nodes
        """
        props = props or {}
        
        try:
            # Execute component with props
            result = component_func(**props)
            
            # Handle different component types
            if isinstance(result, str):
                # Plain HTML string
                return result
            elif isinstance(result, PSXElement):
                # PSX Element - render with PSX renderer using component state context
                from .psx.components import get_current_component
                try:
                    component_state = get_current_component()
                    context = {**props, **component_state.state}
                    return render_psx(result, context)
                except:
                    # Fallback to props if component state not available
                    return render_psx(result)
            elif isinstance(result, VNode):
                # Virtual DOM node - render with VDOM renderer
                return render(result)
            elif hasattr(result, '__html__'):
                # Object with __html__ method
                return result.__html__()
            elif hasattr(result, 'to_html'):
                # PSX Element with to_html method - use component state as context
                from .psx.components import get_current_component
                try:
                    component_state = get_current_component()
                    context = {**props, **component_state.state}
                    return result.to_html(context)
                except:
                    # Fallback to props if component state not available
                    return result.to_html(props)
            elif callable(result):
                # Function component - call it
                return self.render_component(result, props)
            else:
                # Convert to string
                return str(result)
                
        except Exception as e:
            # Error handling with fallback
            error_html = f"""
            <div class="psx-error" style="border: 2px solid red; padding: 10px; margin: 10px;">
                <h3>PSX Component Rendering Error</h3>
                <p><strong>Component:</strong> {component_func.__name__ if hasattr(component_func, '__name__') else 'Unknown'}</p>
                <p><strong>Error:</strong> {str(e)}</p>
                <p><strong>Props:</strong> {props}</p>
            </div>
            """
            return error_html
            
    def render_psx_component(
        self,
        psx_code: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Render PSX code directly with context
        """
        context = context or {}
        
        try:
            # DEBUG: Check if this is an interactive component
            has_decorator = '@interactive_component' in psx_code
            if has_decorator:
                # For interactive components, we need to execute the code and get the component function
                # Create a temporary module to execute the PSX code
                import types
                import tempfile
                import os
                
                # Create temporary file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(psx_code)
                    temp_file = f.name
                
                try:
                    # Import the temporary module
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("temp_psx", temp_file)
                    temp_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(temp_module)
                    
                    # Get the component function (usually 'default' or the first function)
                    component_func = getattr(temp_module, 'default', None)
                    if not component_func:
                        # Find the first callable that might be the component
                        for attr_name in dir(temp_module):
                            attr = getattr(temp_module, attr_name)
                            if callable(attr) and hasattr(attr, '__wrapped__'):
                                component_func = attr
                                break
                    
                    if component_func:
                        # Call the interactive component
                        result = component_func(context.get('props', {}))
                        
                        # The result should be an InteractiveComponentResult
                        if hasattr(result, 'to_html'):
                            return result.to_html()
                        else:
                            return f"<div class='psx-error'>Component function returned: {type(result)} - {str(result)[:200]}</div>"
                    else:
                        return f"<div class='psx-error'>No component function found in interactive PSX. Available attributes: {[attr for attr in dir(temp_module) if not attr.startswith('_')]}</div>"
                        
                except Exception as e:
                    return f"<div class='psx-error'>Error executing interactive PSX: {str(e)}</div>"
                finally:
                    # Clean up temp file
                    os.unlink(temp_file)
            else:
                # Regular PSX component - compile and render
                compiled = compile_psx(psx_code)
                
                # Execute with context
                result = compiled(**context)
                
                # Render result
                if isinstance(result, PSXElement):
                    return render_psx(result)
                elif isinstance(result, VNode):
                    return render(result)
                else:
                    return str(result)
                
        except Exception as e:
            return f"<div class='psx-error'>PSX Rendering Error: {str(e)}</div>"
    
    def render_page(
        self,
        page_module: Any,
        context: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Enhanced page renderer with complete PSX support
        Pages can be:
        1. PSX components using @component decorator
        2. Python functions returning PSX elements
        3. Traditional Jinja2 templates
        4. Mixed PSX + Jinja2
        """
        context = context or {}
        params = params or {}
        
        # Add params to context
        context["params"] = params
        context["renderer"] = self  # Allow pages to access renderer
        
        try:
            # Try PSX component first (preferred method)
            if hasattr(page_module, "Page"):
                return self.render_component(page_module.Page, context)
            
            # Try template function
            if hasattr(page_module, "template"):
                result = page_module.template(**context)
                
                # If template returns PSX element, render it
                if isinstance(result, PSXElement):
                    return render_psx(result)
                elif isinstance(result, VNode):
                    return render(result)
                else:
                    return result
            
            # Try get_template method (traditional Jinja2)
            if hasattr(page_module, "get_template"):
                template_name = page_module.get_template()
                return self.render_template(template_name, context)
            
            # Try rendering as PSX file
            if hasattr(page_module, '__file__'):
                file_path = Path(page_module.__file__)
                if file_path.suffix in ['.py', '.psx']:
                    # Try to read and render as PSX
                    return self._render_psx_file(file_path, context)
            
            # Fallback: try to call the module itself
            if callable(page_module):
                return self.render_component(page_module, context)
            
            raise ValueError(f"Cannot render page module: {page_module}")
            
        except Exception as e:
            # Enhanced error handling
            error_context = {
                'page_module': getattr(page_module, '__name__', 'Unknown'),
                'context': context,
                'params': params,
                'error': str(e)
            }
            
            return self._render_error_page(error_context)
    
    def _render_psx_file(self, file_path: Path, context: Dict[str, Any]) -> str:
        """Render a PSX file directly"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.render_psx_component(content, context)
            
        except Exception as e:
            return f"<div class='psx-error'>PSX File Error: {str(e)}</div>"
    
    def _render_error_page(self, error_context: Dict[str, Any]) -> str:
        """Render an error page with debugging information"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>NextPy PSX Rendering Error</title>
            <style>
                .error-container {{ 
                    max-width: 800px; 
                    margin: 50px auto; 
                    padding: 20px; 
                    border: 2px solid #ff6b6b; 
                    border-radius: 8px; 
                    font-family: monospace; 
                }}
                .error-title {{ color: #ff6b6b; }}
                .error-details {{ background: #f8f9fa; padding: 15px; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <h2 class="error-title">🚨 NextPy PSX Rendering Error</h2>
                <div class="error-details">
                    <p><strong>Page Module:</strong> {error_context.get('page_module', 'Unknown')}</p>
                    <p><strong>Error:</strong> {error_context.get('error', 'Unknown error')}</p>
                    <p><strong>Context:</strong> {error_context.get('context', {})}</p>
                    <p><strong>Params:</strong> {error_context.get('params', {})}</p>
                </div>
                <p><small>This error occurred while trying to render a NextPy page with PSX.</small></p>
            </div>
        </body>
        </html>
        """
        
    def render_template(self, template_name: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Render a Jinja2 template with PSX support"""
        context = context or {}
        
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except TemplateNotFound:
            # Try to find template with .html extension
            if not template_name.endswith('.html'):
                return self.render_template(template_name + '.html', context)
            raise
        except Exception as e:
            return f"<div class='template-error'>Template Error: {str(e)}</div>"
        
    def get_layout_chain(self, page_path: Path) -> List[str]:
        """
        Get the chain of layouts for a page
        Similar to Next.js app router layouts
        """
        layouts = []
        current = page_path.parent
        
        while current != self.pages_dir.parent:
            layout_file = current / "_layout.html"
            if layout_file.exists():
                layouts.append(str(layout_file.relative_to(self.templates_dir)))
            current = current.parent
            
        layouts.reverse()
        
        if (self.templates_dir / "_base.html").exists():
            layouts.insert(0, "_base.html")
            
        return layouts
