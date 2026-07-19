"""
True JSX Parser for Python - Parse actual JSX syntax in Python files
Allows writing <div>...</div> directly in Python code
"""

import re
import ast
import inspect
from typing import Any, Dict, List, Union
from dataclasses import dataclass


@dataclass
class JSXElement:
    """Represents a JSX element"""
    tag: str
    props: Dict[str, Any]
    children: List[Union[str, 'JSXElement']]
    
    def __str__(self) -> str:
        """Convert to HTML string"""
        return self.to_html()
    
    def to_html(self, context: Dict[str, Any] = None) -> str:
        """Convert JSX element to HTML string.

        Evaluates any {expressions} in text nodes and prop values using `context`.
        """
        # Build props string
        props_str = ""
        if self.props:
            props_list = []
            for key, value in self.props.items():
                # Map React-style `className` to HTML `class`
                attr_name = 'class' if key == 'className' else key

                # Boolean attribute
                if isinstance(value, bool) and value:
                    props_list.append(attr_name)
                elif value is not None and value != "":
                    # Skip event handlers
                    if key.startswith("on_") and callable(value):
                        continue

                    # If value looks like a stored expression token '{expr}', evaluate at render time
                    if isinstance(value, str) and value.startswith('{') and value.endswith('}') and context is not None:
                        inner = value[1:-1].strip()
                        try:
                            evaluated = str(eval(inner, {}, context))
                        except Exception:
                            evaluated = ''
                        props_list.append(f'{attr_name}="{evaluated}"')
                    # If string contains inline {expr} parts, evaluate those
                    elif isinstance(value, str) and '{' in value and '}' in value and context is not None:
                        from re import sub
                        evaluated = _evaluate_expressions_in_string(value, context)
                        props_list.append(f'{attr_name}="{evaluated}"')
                    else:
                        props_list.append(f'{attr_name}="{value}"')

            props_str = " " + " ".join(props_list) if props_list else ""

        # Build children string
        children_str = ""
        if self.children:
            children_parts = []
            for child in self.children:
                if isinstance(child, JSXElement):
                    children_parts.append(child.to_html(context))
                else:
                    # Evaluate any {expressions} inside text nodes
                    if isinstance(child, str) and '{' in child and '}' in child and context is not None:
                        children_parts.append(_evaluate_expressions_in_string(child, context))
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


class JSXParser:
    """Parse JSX syntax from Python source code"""
    
    def __init__(self):
        self.jsx_pattern = re.compile(r'<([a-zA-Z][a-zA-Z0-9]*)\s*([^>]*)>(.*?)</\1>', re.DOTALL)
        self.self_closing_pattern = re.compile(r'<([a-zA-Z][a-zA-Z0-9]*)\s*([^>]*)\s*/>', re.DOTALL)
        self.prop_pattern = re.compile(r'([a-zA-Z][a-zA-Z0-9-]*)\s*=\s*\{([^}]+)\}|([a-zA-Z][a-zA-Z0-9-]*)\s*=\s*"([^"]*)"|([a-zA-Z][a-zA-Z0-9-]*)\s*=\s*\'([^\']*)\'|([a-zA-Z][a-zA-Z0-9-]+)')
    
    def parse_props(self, props_str: str) -> Dict[str, Any]:
        """Parse JSX props string"""
        props = {}
        if not props_str.strip():
            return props
        
        # Simple prop parsing - can be enhanced
        for match in self.prop_pattern.finditer(props_str):
            groups = match.groups()
            if groups[0] and groups[1]:  # {prop} syntax
                prop_name = groups[0]
                prop_value = groups[1].strip()
                # Store as a raw expression token to be evaluated at render time
                props[prop_name] = '{' + prop_value + '}'
            elif groups[2] and groups[3]:  # "prop" syntax
                props[groups[2]] = groups[3]
            elif groups[4] and groups[5]:  # 'prop' syntax
                props[groups[4]] = groups[5]
            elif groups[6]:  # prop without value (boolean)
                props[groups[6]] = True
        
        return props
    
    def parse_jsx(self, jsx_str: str) -> JSXElement:
        """Parse JSX string to JSXElement"""
        jsx_str = jsx_str.strip()
        
        # Try self-closing tag first
        self_closing_match = self.self_closing_pattern.match(jsx_str)
        if self_closing_match:
            tag = self_closing_match.group(1)
            props_str = self_closing_match.group(2)
            props = self.parse_props(props_str)
            return JSXElement(tag, props, [])
        
        # Try regular tag
        match = self.jsx_pattern.match(jsx_str)
        if match:
            tag = match.group(1)
            props_str = match.group(2)
            children_str = match.group(3)
            
            props = self.parse_props(props_str)
            children = self.parse_children(children_str)
            
            return JSXElement(tag, props, children)
        
        # If no JSX tags found, treat as text
        return jsx_str
    
    def parse_children(self, children_str: str) -> List[Union[str, JSXElement]]:
        """Parse children string"""
        children = []
        
        # Split by JSX tags and text
        parts = re.split(r'(<[^>]+>)', children_str)
        
        i = 0
        while i < len(parts):
            part = parts[i].strip()
            
            if not part:
                i += 1
                continue
            
            # Check if it's an opening tag
            if part.startswith('<') and not part.startswith('</'):
                # Find the matching closing tag
                tag_match = re.match(r'<([a-zA-Z][a-zA-Z0-9]*)', part)
                if tag_match:
                    tag = tag_match.group(1)
                    # Find the complete JSX element
                    jsx_content = part
                    depth = 1
                    j = i + 1
                    
                    while j < len(parts) and depth > 0:
                        if parts[j].startswith(f'</{tag}>'):
                            depth -= 1
                        elif parts[j].startswith(f'<{tag}') and not parts[j].startswith('</'):
                            depth += 1
                        jsx_content += parts[j]
                        j += 1
                    
                    children.append(self.parse_jsx(jsx_content))
                    i = j - 1
                else:
                    children.append(part)
            elif part.startswith('</'):
                # Closing tag - skip
                pass
            else:
                # Text content
                if part:
                    children.append(part)
            
            i += 1
        
        return children


# Global parser instance
parser = JSXParser()


def jsx(jsx_str: str) -> JSXElement:
    """Parse JSX string to JSXElement"""
    return parser.parse_jsx(jsx_str)


def _evaluate_expressions_in_string(s: str, context: Dict[str, Any]) -> str:
    """Find {expressions} in string `s` and evaluate them using `context`."""
    def repl(match):
        expr = match.group(1).strip()
        try:
            return str(eval(expr, {}, context or {}))
        except Exception:
            return ''

    return re.sub(r'\{([^}]+)\}', repl, s)


def render_jsx(element, context: Dict[str, Any] = None) -> str:
    """Render JSX element to HTML string, evaluating {expressions} with `context`.

    Usage: `render_jsx(element, context)`
    """
    if isinstance(element, JSXElement):
        return element.to_html(context)
    elif isinstance(element, str):
        if context and '{' in element and '}' in element:
            return _evaluate_expressions_in_string(element, context)
        return element
    else:
        return str(element)


class Component:
    """Base class for JSX components"""
    
    def render(self) -> JSXElement:
        """Override this method to define component rendering"""
        raise NotImplementedError("Component must implement render method")
    
    def __call__(self) -> JSXElement:
        """Make component callable"""
        return self.render()


def create_jsx_function(jsx_str: str):
    """Create a function that returns parsed JSX"""
    def jsx_func():
        return jsx(jsx_str)
    return jsx_func


# Decorator for components with JSX
def JSXComponent(func):
    """Decorator to create a component with JSX syntax"""
    def wrapper(*args, **kwargs):
        # Get the source code of the function
        source = inspect.getsource(func)
        
        # Extract JSX from return statement
        jsx_match = re.search(r'return\s*\(\s*(<.*?>)\s*\)', source, re.DOTALL)
        if jsx_match:
            jsx_str = jsx_match.group(1)
            return jsx(jsx_str)
        else:
            # Try to find JSX without parentheses
            jsx_match = re.search(r'return\s*(<.*?>)', source, re.DOTALL)
            if jsx_match:
                jsx_str = jsx_match.group(1)
                return jsx(jsx_str)
        
        # Fallback to regular function call
        return func(*args, **kwargs)
    
    return wrapper
