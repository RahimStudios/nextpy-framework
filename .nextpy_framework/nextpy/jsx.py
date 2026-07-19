"""
NextPy JSX - JSX-like syntax for Python components
Allows writing HTML-like structures in Python, similar to React/Next.js JSX
"""

from typing import Any, Dict, List, Union, Optional
from dataclasses import dataclass
import re
from .security import security_manager


@dataclass
class JSXElement:
    """Represents a JSX element with tag, props, and children"""
    tag: str
    props: Dict[str, Any]
    children: List[Union[str, 'JSXElement']]

    def __str__(self) -> str:
        """Convert JSX element to HTML string"""
        return self.to_html()

    def to_html(self) -> str:
        """Convert JSX element to HTML string with XSS protection"""
        # Sanitize props to prevent XSS
        sanitized_props = security_manager.sanitize_jsx_props(self.props)
        
        # Build props string
        props_str = ""
        if sanitized_props:
            props_list = []
            for key, value in sanitized_props.items():
                if isinstance(value, bool) and value:
                    props_list.append(key)
                elif value is not None and value != "":
                    if key.startswith("on_") and callable(value):
                        # Skip event handlers for now
                        continue
                    # Additional XSS protection for href/src attributes
                    if key in ['href', 'src', 'action'] and isinstance(value, str):
                        if not security_manager.validate_url(value):
                            continue
                    props_list.append(f'{key}="{value}"')
            props_str = " " + " ".join(props_list) if props_list else ""

        # Build children string with XSS protection
        children_str = ""
        if self.children:
            children_parts = []
            for child in self.children:
                if isinstance(child, JSXElement):
                    children_parts.append(child.to_html())
                else:
                    # Sanitize text content to prevent XSS
                    if isinstance(child, str):
                        children_parts.append(security_manager.sanitize_html(child))
                    else:
                        children_parts.append(str(child))
            children_str = "".join(children_parts)

        # Handle self-closing tags
        self_closing_tags = {
            'img', 'br', 'hr', 'input', 'meta', 'link', 'area', 'base', 'col', 
            'embed', 'source', 'track', 'wbr', 'command', 'keygen', 'menuitem', 'param'
        }
        
        if self.tag in self_closing_tags and not children_str:
            return f"<{self.tag}{props_str} />"
        
        return f"<{self.tag}{props_str}>{children_str}</{self.tag}>"


def jsx(tag: str, props: Optional[Dict[str, Any]] = None, *children) -> JSXElement:
    """
    Create a JSX element
    Usage: jsx('div', {'className': 'container'}, 'Hello', jsx('span', None, 'World'))
    """
    if props is None:
        props = {}
    
    # Flatten children
    flat_children = []
    for child in children:
        if isinstance(child, (list, tuple)):
            flat_children.extend(child)
        elif child is not None and child != "":
            flat_children.append(child)
    
    return JSXElement(tag, props, flat_children)


def Fragment(*children) -> JSXElement:
    """React Fragment equivalent"""
    return jsx('fragment', {}, *children)


# Create HTML element functions for common tags
def create_element_function(tag: str):
    """Create a function for a specific HTML tag"""
    def element_func(props=None, *children):
        if props is None:
            props = {}
        return jsx(tag, props, *children)
    return element_func


# Generate HTML element functions
HTML_TAGS = [
    'a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base',
    'bdi', 'bdo', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption',
    'cite', 'code', 'col', 'colgroup', 'data', 'datalist', 'dd', 'del',
    'details', 'dfn', 'dialog', 'div', 'dl', 'dt', 'em', 'embed', 'fieldset',
    'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'head', 'header', 'hgroup', 'hr', 'html', 'i', 'iframe', 'img', 'input',
    'ins', 'kbd', 'label', 'legend', 'li', 'link', 'main', 'map', 'mark',
    'meta', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup', 'option',
    'output', 'p', 'param', 'picture', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby',
    's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span',
    'strong', 'style', 'sub', 'summary', 'sup', 'table', 'tbody', 'td',
    'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr',
    'track', 'u', 'ul', 'var', 'video', 'wbr'
]

# Create functions for all HTML tags
for tag in HTML_TAGS:
    globals()[tag] = create_element_function(tag)


def render_jsx(component) -> str:
    """Render a JSX component to HTML string"""
    if isinstance(component, JSXElement):
        return component.to_html()
    elif callable(component):
        # If it's a function, call it and render the result
        result = component()
        return render_jsx(result)
    else:
        return str(component)


class Component:
    """Base class for NextPy components"""
    
    def render(self) -> JSXElement:
        """Override this method to define component rendering"""
        raise NotImplementedError("Component must implement render method")
    
    def __call__(self) -> JSXElement:
        """Make component callable"""
        return self.render()


def create_component(render_func):
    """Create a component from a render function"""
    class FuncComponent(Component):
        def render(self) -> JSXElement:
            return render_func(self)
    
    return FuncComponent()


# Helper functions for common patterns
def map_children(children, func):
    """Map over children and apply function"""
    return [func(child) for child in children]


def clone_element(element, new_props=None, *new_children):
    """Clone an element with new props and/or children"""
    if new_props is None:
        new_props = {}
    
    props = {**element.props, **new_props}
    children = new_children if new_children else element.children
    
    return JSXElement(element.tag, props, children)


# CSS-in-JS support
def css(**styles) -> str:
    """Convert CSS properties to inline style string"""
    style_parts = []
    for prop, value in styles.items():
        # Convert camelCase to kebab-case
        kebab_prop = re.sub(r'(?<!^)(?=[A-Z])', '-', prop).lower()
        style_parts.append(f"{kebab_prop}: {value}")
    
    return "; ".join(style_parts)
