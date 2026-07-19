"""
PSX Server & Client Components System
Following Next.js App Router pattern:
- Server Components (default): Rendered exclusively on server
- Client Components (opt-in): Rendered on both server and client with "use client" directive
"""

import threading
import uuid
import inspect
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from functools import wraps
from ..core.vnode import VNode, create_element, render
from ..core.parser import PSXElement, psx, render_psx


@dataclass
class ComponentMetadata:
    """Metadata for PSX components"""
    is_client: bool = False  # False = Server Component (default), True = Client Component
    component_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    has_interactivity: bool = False  # Tracks if component uses hooks like useState, useEffect
    javascript_bundles: List[str] = field(default_factory=list)


# Thread-local storage for component metadata
_component_metadata = threading.local()


def get_component_metadata() -> ComponentMetadata:
    """Get current component's metadata"""
    if not hasattr(_component_metadata, 'current'):
        _component_metadata.current = {}
    
    thread_id = threading.get_ident()
    if thread_id not in _component_metadata.current:
        _component_metadata.current[thread_id] = ComponentMetadata()
    
    return _component_metadata.current[thread_id]


def set_component_metadata(metadata: ComponentMetadata):
    """Set component metadata"""
    thread_id = threading.get_ident()
    if not hasattr(_component_metadata, 'current'):
        _component_metadata.current = {}
    _component_metadata.current[thread_id] = metadata


def reset_component_metadata():
    """Reset component metadata for new render"""
    if hasattr(_component_metadata, 'current'):
        thread_id = threading.get_ident()
        if thread_id in _component_metadata.current:
            _component_metadata.current[thread_id] = ComponentMetadata()


def parse_use_client_directive(source_code: str) -> bool:
    """
    Parse source code for "use client" directive
    Returns True if "use client" is found at the top of the file
    """
    lines = source_code.strip().split('\n')
    for line in lines[:5]:  # Check first 5 lines
        stripped = line.strip()
        # Check for various forms of "use client" directive
        if (stripped == '"use client"' or 
            stripped == "'use client'" or 
            stripped.startswith('use client') or
            stripped == '# use client' or
            stripped.startswith('# use client')):
            return True
    return False


def server_component(func):
    """
    Decorator to explicitly mark a component as Server Component
    Server Components are rendered exclusively on the server
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Reset and set metadata
        reset_component_metadata()
        metadata = get_component_metadata()
        metadata.is_client = False
        
        # Execute component
        result = func(*args, **kwargs)
        
        # Server components should not contain client-side hooks
        # This is a safety check
        if metadata.has_interactivity:
            raise ValueError("Server Components cannot use client-side hooks like useState or useEffect")
        
        return result
    
    wrapper._is_server_component = True
    wrapper._is_psx_component = True
    return wrapper


def client_component(func):
    """
    Decorator to explicitly mark a component as Client Component
    Client Components are rendered on both server and client
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Reset and set metadata
        reset_component_metadata()
        metadata = get_component_metadata()
        metadata.is_client = True
        
        # Execute component
        result = func(*args, **kwargs)
        
        return result
    
    wrapper._is_client_component = True
    wrapper._is_psx_component = True
    return wrapper


def component(func):
    """
    Default component decorator - creates Server Component by default
    Automatically detects "use client" directive to create Client Component
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Reset metadata
        reset_component_metadata()
        metadata = get_component_metadata()
        
        # Check for "use client" directive in source code
        is_client = parse_use_client_directive(inspect.getsource(func))
        
        metadata.is_client = is_client
        
        # Execute component
        result = func(*args, **kwargs)
        
        return result
    
    wrapper._is_psx_component = True
    wrapper._component_type = 'client' if parse_use_client_directive(inspect.getsource(func)) else 'server'
    return wrapper


class ComponentRenderer:
    """
    Enhanced component renderer that handles Server and Client Components
    Following Next.js App Router pattern
    """
    
    def __init__(self):
        self.server_component_cache = {}
        self.client_component_registry = {}
    
    def render_server_component(self, component_func, props: Dict[str, Any]) -> str:
        """
        Render a Server Component exclusively on the server
        Server Components:
        - Have access to server-side resources (databases, file system)
        - Do not send JavaScript to client
        - Are rendered to HTML on server
        - Can be static (build time) or dynamic (request time)
        """
        # Mark as server component
        reset_component_metadata()
        metadata = get_component_metadata()
        metadata.is_client = False
        
        # Execute server component
        if hasattr(component_func, '_is_psx_component'):
            result = component_func(props)
        else:
            result = component_func(**props)
        
        # Convert to HTML
        if isinstance(result, PSXElement):
            html = result.to_html(props)
        elif isinstance(result, str):
            html = render_psx(result, props)
        else:
            html = str(result)
        
        return html
    
    def render_client_component(self, component_func, props: Dict[str, Any]) -> Dict[str, Any]:
        """
        Render a Client Component
        Client Components:
        - Are pre-rendered to HTML on server for fast initial load
        - Include JavaScript for interactivity
        - Support hooks like useState, useEffect
        - Handle user interactions on client side
        """
        # Mark as client component
        reset_component_metadata()
        metadata = get_component_metadata()
        metadata.is_client = True
        
        # Execute client component (server-side pre-render)
        if hasattr(component_func, '_is_psx_component'):
            result = component_func(props)
        else:
            result = component_func(**props)
        
        # Convert to HTML for initial server render
        if isinstance(result, PSXElement):
            html = result.to_html(props)
        elif isinstance(result, str):
            html = render_psx(result, props)
        else:
            html = str(result)
        
        # Prepare client component data
        client_data = {
            'html': html,
            'component_id': metadata.component_id,
            'props': props,
            'is_client': True,
            'javascript_bundles': metadata.javascript_bundles,
            'has_interactivity': metadata.has_interactivity
        }
        
        return client_data
    
    def render_component(self, component_func, props: Dict[str, Any] = None) -> Union[str, Dict[str, Any]]:
        """
        Main render method that determines component type and renders accordingly
        """
        props = props or {}
        
        # Check component type
        is_client = False
        
        if hasattr(component_func, '_is_client_component'):
            is_client = True
        elif hasattr(component_func, '_is_server_component'):
            is_client = False
        elif hasattr(component_func, '_component_type'):
            is_client = component_func._component_type == 'client'
        else:
            # Check source code for "use client" directive
            try:
                is_client = parse_use_client_directive(inspect.getsource(component_func))
            except:
                is_client = False
        
        # Render based on component type
        if is_client:
            return self.render_client_component(component_func, props)
        else:
            return self.render_server_component(component_func, props)


# Global renderer instance
component_renderer = ComponentRenderer()


# Convenience functions
def render_server_component(component_func, props: Dict[str, Any] = None) -> str:
    """Render a Server Component"""
    return component_renderer.render_server_component(component_func, props or {})


def render_client_component(component_func, props: Dict[str, Any] = None) -> Dict[str, Any]:
    """Render a Client Component"""
    return component_renderer.render_client_component(component_func, props or {})


def render_component(component_func, props: Dict[str, Any] = None) -> Union[str, Dict[str, Any]]:
    """Render a component (auto-detects Server vs Client)"""
    return component_renderer.render_component(component_func, props or {})


# Hook detection for client components
def mark_interactive():
    """Mark current component as interactive (uses client-side hooks)"""
    metadata = get_component_metadata()
    metadata.has_interactivity = True


def add_javascript_bundle(bundle_path: str):
    """Add JavaScript bundle to client component"""
    metadata = get_component_metadata()
    if bundle_path not in metadata.javascript_bundles:
        metadata.javascript_bundles.append(bundle_path)
