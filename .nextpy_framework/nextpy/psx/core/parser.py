"""
PSX Parser - Production-grade parser with AST integration
Supports full PSX capability with modern architecture
"""

import re
import json
from typing import Any, Dict, List, Union, Optional, Tuple
from dataclasses import dataclass, field
from .ast_nodes import (
    PSXNode, PSXNodeUnion, NodeType, LogicType,
    ElementNode, TextNode, ExpressionNode, LogicNode,
    IfNode, ForNode, WhileNode, TryNode,
    ComponentNode, FragmentNode,
    PSXASTParser, PSXNodeValidator, PSXNodeOptimizer
)
from .runtime import PSXRuntime, process_python_logic


@dataclass
class PSXElement:
    """Legacy PSX element - maintained for backwards compatibility"""
    tag: str
    props: Dict[str, Any] = field(default_factory=dict)
    children: List[Union[str, 'PSXElement']] = field(default_factory=list)
    key: Optional[str] = None
    
    def to_ast(self) -> ElementNode:
        """Convert legacy PSXElement to production-grade AST"""
        # Separate events from props
        events = {}
        attributes = {}
        
        for key, value in self.props.items():
            if key.startswith('on') and callable(value):
                events[key] = value.__name__
            else:
                attributes[key] = value
        
        # Convert children
        ast_children = []
        for child in self.children:
            if isinstance(child, str):
                ast_children.append(TextNode(content=child))
            elif isinstance(child, PSXElement):
                ast_children.append(child.to_ast())
        
        return ElementNode(
            tag=self.tag,
            attributes=attributes,
            events=events,
            children=ast_children,
            key=self.key,
            self_closing=self.tag in {
                'img', 'br', 'hr', 'input', 'meta', 'link', 'area', 'base', 'col',
                'embed', 'source', 'track', 'wbr', 'command', 'keygen', 'menuitem', 'param'
            }
        )
    
    def to_html(self, context: Dict[str, Any] = None) -> str:
        """Convert PSX element to HTML string"""
        # Use stored AST node if available, otherwise use stored context
        if hasattr(self, '_ast_node') and self._ast_node:
            # Use stored context if available, otherwise use provided context
            if hasattr(self, '_psx_context') and self._psx_context:
                render_context = self._psx_context
            elif context:
                render_context = context
            else:
                render_context = {}
            
            runtime = PSXRuntime(render_context)
            return runtime._render_node(self._ast_node)
        else:
            # Fallback to legacy behavior
            # Use stored context if available, otherwise use provided context
            if hasattr(self, '_psx_context') and self._psx_context:
                context = self._psx_context
            elif context:
                # Use provided context
                pass
            else:
                context = {}
            
            runtime = PSXRuntime(context)
            
            # Convert to AST and render
            ast_node = self.to_ast()
            return runtime._render_node(ast_node)


class PSXParser:
    """Production-grade PSX parser with AST integration"""
    
    def __init__(self):
        self.ast_parser = PSXASTParser()
        self.validator = PSXNodeValidator()
        self.optimizer = PSXNodeOptimizer()
        self.runtime = PSXRuntime()
        
        # Regex patterns for parsing - use non-greedy matching
        self.psx_pattern = re.compile(r'<([a-zA-Z][a-zA-Z0-9:_-]*)\s*([^>]*?)>(.*?)</\1>', re.DOTALL)
        self.self_closing_pattern = re.compile(r'<([a-zA-Z][a-zA-Z0-9:_-]*)\s*([^>]*?)\s*/>', re.DOTALL)
        self.prop_pattern = re.compile(
            r'([a-zA-Z][a-zA-Z0-9:_-]*)\s*=\s*\{([^}]+)\}|'
            r'([a-zA-Z][a-zA-Z0-9:_-]*)\s*=\s*"([^"]*)"|'
            r'([a-zA-Z][a-zA-Z0-9:_-]*)\s*=\s*\'([^\']*)\'|'
            r'([a-zA-Z][a-zA-Z0-9:_-]+)|'
            r'\.{3}[a-zA-Z_][a-zA-Z0-9_:-]*'  # Spread props
        )
    
    def parse_psx(self, psx_str: str, context: Dict[str, Any] = None) -> PSXNodeUnion:
        """Parse PSX string to production-grade AST node"""
        context = context or {}
        
        # Update runtime context with new variables
        self.runtime.update_context(context)
        
        # Process Python logic first
        psx_str = process_python_logic(psx_str, context)
        
        # Normalize whitespace for parsing while preserving original content if needed
        psx_str_stripped = psx_str.strip()
        
        # Try to parse as fragment first, since fragments use special shorthand syntax
        ast_node = self._parse_fragment(psx_str_stripped, context)
        if ast_node:
            return self.optimizer.optimize_node(ast_node)

        # Try to parse as component next
        ast_node = self._parse_component(psx_str_stripped, context)
        if ast_node:
            return self.optimizer.optimize_node(ast_node)

        # Try to parse as element last
        ast_node = self._parse_element(psx_str_stripped, context)
        if ast_node:
            return self.optimizer.optimize_node(ast_node)
        
        # Default to text node
        return TextNode(content=psx_str)
    
    def _parse_element(self, psx_str: str, context: Dict[str, Any]) -> Optional[ElementNode]:
        """Robust recursive element parser for minified JSX"""
        # Strip leading whitespace for better matching
        psx_str_stripped = psx_str.strip()
        
        if not psx_str_stripped.startswith('<'):
            return None
        
        try:
            element_node, final_index = self._parse_element_recursive(psx_str_stripped, 0, context)
            return element_node
        except Exception as e:
            # Fallback to original method if recursive parsing fails
            return self._parse_element_fallback(psx_str_stripped, context)
    
    def _parse_element_recursive(self, code: str, index: int, context: Dict[str, Any]):
        """Recursive descent parser for JSX elements"""
        from .ast_nodes import ElementNode
        
        # Skip opening '<'
        index += 1
        
        # Read tag name
        tag_name, index = self._read_tag_name(code, index)
        
        # Read attributes until closing '>' or '/>'
        attributes, events, spread_props, index = self._read_attributes(code, index, context)
        
        # Check if self-closing
        if index < len(code) and code[index-2:index] == '/>':
            return ElementNode(
                tag=tag_name,
                attributes=attributes,
                events=events,
                children=[],
                self_closing=True,
                spread_props=spread_props
            ), index
        
        # Parse children recursively
        children = []
        while index < len(code) and not code.startswith(f"</{tag_name}>", index):
            # Process Python logic for the current segment of code before parsing nodes
            # This ensures nested control flow is handled correctly
            remaining_code = code[index:]
            # Find next tag or expression to limit processing scope if possible, 
            # but for now, we process the logic which is safe as it uses brace matching.
            
            child, index = self._parse_node(code, index, context)
            if child:
                if isinstance(child, TextNode):
                    # Re-process text nodes for any missed logic
                    child.content = process_python_logic(child.content, context)
                children.append(child)
        
        # Skip closing tag
        if index < len(code) and code.startswith(f"</{tag_name}>", index):
            index += len(f"</{tag_name}>")
        
        return ElementNode(
            tag=tag_name,
            attributes=attributes,
            events=events,
            children=children,
            spread_props=spread_props
        ), index
    
    def _read_tag_name(self, code: str, index: int):
        """Read tag name from code"""
        start = index
        while index < len(code) and (code[index].isalnum() or code[index] in '-_:'):
            index += 1
        return code[start:index], index
    
    def _read_attributes(self, code: str, index: int, context: Dict[str, Any]):
        """Read attributes from opening tag"""
        attributes = {}
        events = {}
        spread_props = []
        
        while index < len(code) and code[index] not in ['>', '/']:
            # Skip whitespace
            while index < len(code) and code[index].isspace():
                index += 1
            
            if index >= len(code) or code[index] in ['>', '/']:
                break
            
            # Read attribute name
            key_start = index
            while index < len(code) and (code[index].isalnum() or code[index] in '-_:.'):
                index += 1
            key = code[key_start:index]
            
            # Skip whitespace
            while index < len(code) and code[index].isspace():
                index += 1
            
            # Check if attribute has value
            if index < len(code) and code[index] == '=':
                index += 1  # Skip '='
                
                # Skip whitespace
                while index < len(code) and code[index].isspace():
                    index += 1
                
                # Read value
                if index < len(code) and code[index] in ['"', "'"]:
                    # String value
                    quote = code[index]
                    index += 1
                    value_start = index
                    while index < len(code) and code[index] != quote:
                        index += 1
                    value = code[value_start:index]
                    index += 1  # Skip closing quote
                elif index < len(code) and code[index] == '{':
                    # Expression value
                    value_start = index
                    brace_count = 1
                    index += 1
                    while index < len(code) and brace_count > 0:
                        if code[index] == '{':
                            brace_count += 1
                        elif code[index] == '}':
                            brace_count -= 1
                        index += 1
                    value = code[value_start:index]
                else:
                    # Unquoted value (boolean or simple)
                    value_start = index
                    while index < len(code) and not code[index].isspace() and code[index] not in ['>', '/']:
                        index += 1
                    value = code[value_start:index]
                
                # Categorize attribute
                if key.startswith('on'):
                    events[key] = value
                elif key.startswith('...'):
                    spread_props.append(key[3:])
                else:
                    attributes[key] = value
            else:
                # Boolean attribute
                attributes[key] = True
        
        return attributes, events, spread_props, index
    
    def _parse_node(self, code: str, index: int, context: Dict[str, Any]):
        """Parse node (element, text, or expression)"""
        # Skip whitespace
        while index < len(code) and code[index].isspace():
            index += 1
        
        if index >= len(code):
            return None, index
        
        if code[index] == '<':
            # Element node
            if code.startswith('<!--', index):
                # Comment - skip it
                end_comment = code.find('-->', index)
                if end_comment != -1:
                    return None, end_comment + 3
                return None, len(code)
            elif code.startswith('</', index):
                # Closing tag - stop parsing
                return None, index
            else:
                # Opening tag
                return self._parse_element_recursive(code, index, context)
        elif code[index] == '{':
            # Expression node
            from .ast_nodes import ExpressionNode
            expr_start = index
            brace_count = 1
            index += 1
            while index < len(code) and brace_count > 0:
                if code[index] == '{':
                    brace_count += 1
                elif code[index] == '}':
                    brace_count -= 1
                index += 1
            expr_content = code[expr_start + 1:index - 1]  # Remove braces
            return ExpressionNode(expression=expr_content), index
        else:
            # Text node
            from .ast_nodes import TextNode
            text_start = index
            while index < len(code) and code[index] not in ['<', '{']:
                index += 1
            text_content = code[text_start:index]
            return TextNode(content=text_content), index
    
    def _parse_element_fallback(self, psx_str: str, context: Dict[str, Any]) -> Optional[ElementNode]:
        """Fallback to original parsing method"""
        # Check for self-closing tags first
        self_closing_match = self.self_closing_pattern.match(psx_str)
        if self_closing_match:
            tag = self_closing_match.group(1)
            props_str = self_closing_match.group(2).strip()
            props = self._parse_props(props_str, context)
            
            return ElementNode(
                tag=tag,
                attributes=props['attributes'],
                events=props['events'],
                children=[],
                self_closing=True,
                spread_props=props['spread_props']
            )
        
        # For regular tags, use the robust approach
        if psx_str.startswith('<'):
            # Find the end of the opening tag
            tag_end = psx_str.find('>')
            if tag_end == -1:
                return None
            
            opening_tag = psx_str[:tag_end + 1]
            tag_content = opening_tag[1:-1].strip()
            
            # Extract tag name and props
            tag_parts = tag_content.split()
            if not tag_parts:
                return None
            
            tag_name = tag_parts[0]
            props_str = ' '.join(tag_parts[1:]) if len(tag_parts) > 1 else ''
            props = self._parse_props(props_str, context)
            
            # Find the matching closing tag
            closing_tag = f'</{tag_name}>'
            closing_pos = self._find_matching_tag(psx_str, tag_name, tag_end + 1)
            
            if closing_pos == -1:
                # No matching closing tag
                return None
            
            # Extract children content
            children_content = psx_str[tag_end + 1:closing_pos]
            children = self._parse_children(children_content, context)
            
            return ElementNode(
                tag=tag_name,
                attributes=props['attributes'],
                events=props['events'],
                children=children,
                spread_props=props['spread_props']
            )
        
        return None
    
    def _parse_component(self, psx_str: str, context: Dict[str, Any]) -> Optional[ComponentNode]:
        """Parse PSX string to ComponentNode"""
        # Component pattern (uppercase first letter)
        component_pattern = re.compile(r'<([A-Z][a-zA-Z0-9]*)\s*([^>]*)>(.*?)</\1>', re.DOTALL)
        
        match = component_pattern.match(psx_str)
        if match:
            name = match.group(1)
            props_str = match.group(2).strip()
            children_str = match.group(3)
            
            props = self._parse_props(props_str, context)
            children = self._parse_children(children_str, context)
            
            return ComponentNode(
                name=name,
                props=props['attributes'],
                events=props['events'],
                children=children,
                spread_props=props['spread_props']
            )
        
        return None
    
    def _parse_fragment(self, psx_str: str, context: Dict[str, Any]) -> Optional[FragmentNode]:
        """Parse PSX string to FragmentNode"""
        psx_str = psx_str.strip()
        # Fragment patterns
        fragment_patterns = [
            re.compile(r'<>\s*(.*?)\s*</>', re.DOTALL),  # Shorthand
            re.compile(r'<fragment\s*[^>]*>\s*(.*?)\s*</fragment>', re.DOTALL)  # Full
        ]
        
        for i, pattern in enumerate(fragment_patterns):
            match = pattern.match(psx_str)
            if match:
                children_str = match.group(1)
                children = self._parse_children(children_str, context)
                
                return FragmentNode(
                    children=children,
                    shorthand=(i == 0)  # First pattern is shorthand
                )
        
        return None
    
    def _parse_props(self, props_str: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse props string into attributes, events, and spread props"""
        attributes = {}
        events = {}
        spread_props = []
        
        if not props_str.strip():
            return {'attributes': attributes, 'events': events, 'spread_props': spread_props}
        
        for match in self.prop_pattern.finditer(props_str):
            groups = match.groups()
            
            if groups[0] and groups[1]:  # {prop} syntax - Python expression
                prop_name = groups[0]
                prop_value = groups[1].strip()
                
                # Parse expression
                parsed_ast = self.ast_parser.parse_expression(prop_value)
                if parsed_ast:
                    if prop_name.startswith('on'):
                        events[prop_name] = prop_value
                    else:
                        attributes[prop_name] = prop_value
                else:
                    attributes[prop_name] = prop_value
                    
            elif groups[2] and groups[3]:  # "prop" syntax
                attributes[groups[2]] = groups[3]
            elif groups[4] and groups[5]:  # 'prop' syntax
                attributes[groups[4]] = groups[5]
            elif groups[6]:  # prop without value (boolean)
                attributes[groups[6]] = True
            elif groups[7]:  # spread props ...props
                spread_name = groups[7][3:]  # Remove ...
                spread_props.append(spread_name)
        
        return {'attributes': attributes, 'events': events, 'spread_props': spread_props}
    
    def _parse_children(self, children_str: str, context: Dict[str, Any]) -> List[PSXNodeUnion]:
        """Parse children string into AST nodes"""
        children = []
        
        # Use a more sophisticated parsing approach
        i = 0
        n = len(children_str)
        
        while i < n:
            # Skip whitespace
            while i < n and children_str[i].isspace():
                i += 1
            
            if i >= n:
                break
            
            # Check for HTML tag
            if children_str[i] == '<':
                # Find the end of the tag
                tag_end = children_str.find('>', i)
                if tag_end == -1:
                    # Malformed tag, treat as text
                    children.append(TextNode(content=children_str[i:]))
                    break
                
                tag_content = children_str[i:tag_end + 1]
                
                # Check if it's a self-closing tag
                if tag_content.endswith('/>'):
                    # Self-closing tag
                    tag_node = self.parse_psx(tag_content, context)
                    if tag_node and not isinstance(tag_node, TextNode):
                        children.append(tag_node)
                        i = tag_end + 1
                    else:
                        children.append(TextNode(content=tag_content))
                        i = tag_end + 1
                else:
                    # Opening tag - find matching closing tag
                    tag_name = tag_content[1:-1].split()[0]  # Extract tag name
                    closing_tag = f'</{tag_name}>'
                    closing_pos = self._find_matching_tag(children_str, tag_name, tag_end + 1)
                    
                    if closing_pos == -1:
                        # No matching closing tag, treat as text
                        children.append(TextNode(content=tag_content))
                        i = tag_end + 1
                    else:
                        # Parse the complete element
                        element_str = children_str[i:closing_pos + len(closing_tag)]
                        element_node = self.parse_psx(element_str, context)
                        if element_node and not isinstance(element_node, TextNode):
                            children.append(element_node)
                            i = closing_pos + len(closing_tag)
                        else:
                            children.append(TextNode(content=element_str))
                            i = closing_pos + len(closing_tag)
            else:
                # Text content - find next tag or expression
                next_tag = children_str.find('<', i)
                next_expr = children_str.find('{', i)
                
                if next_tag == -1 and next_expr == -1:
                    # Plain text to end
                    text_content = children_str[i:].strip()
                    if text_content:
                        text_parts = self._parse_text_with_expressions(text_content)
                        children.extend(text_parts)
                    break
                elif next_tag == -1 or (next_expr != -1 and next_expr < next_tag):
                    # Expression comes first
                    text_content = children_str[i:next_expr].strip()
                    if text_content:
                        children.append(TextNode(content=text_content))
                    
                    # Parse expression
                    expr_end = children_str.find('}', next_expr)
                    if expr_end == -1:
                        # Malformed expression
                        children.append(TextNode(content=children_str[next_expr:]))
                        break
                    
                    expr_content = children_str[next_expr:expr_end + 1]
                    text_parts = self._parse_text_with_expressions(expr_content)
                    children.extend(text_parts)
                    i = expr_end + 1
                else:
                    # Tag comes first
                    text_content = children_str[i:next_tag].strip()
                    if text_content:
                        text_parts = self._parse_text_with_expressions(text_content)
                        children.extend(text_parts)
                    i = next_tag
        
        return children
    
    def _find_matching_tag(self, text: str, tag_name: str, start_pos: int) -> int:
        """Find the position of the matching closing tag"""
        depth = 1
        i = start_pos
        n = len(text)
        
        while i < n and depth > 0:
            # Look for opening tag
            open_tag = f'<{tag_name}'
            close_tag = f'</{tag_name}>'
            
            next_open = text.find(open_tag, i)
            next_close = text.find(close_tag, i)
            
            if next_close == -1:
                return -1  # No matching closing tag
            
            if next_open == -1 or next_close < next_open:
                # Found closing tag
                depth -= 1
                if depth == 0:
                    return next_close
                i = next_close + len(close_tag)
            else:
                # Found opening tag
                depth += 1
                i = next_open + len(open_tag)
        
        return -1  # No match found
    
    def _parse_text_with_expressions(self, text: str) -> List[PSXNodeUnion]:
        """Parse text containing expressions"""
        nodes = []
        
        # Split by expressions
        parts = re.split(r'(\{[^}]+\})', text)
        
        for part in parts:
            if part.startswith('{') and part.endswith('}'):
                # Expression
                expr = part[1:-1].strip()
                parsed_ast = self.ast_parser.parse_expression(expr)
                nodes.append(ExpressionNode(
                    expression=expr,
                    parsed_expression=parsed_ast
                ))
            elif part:
                # Text
                nodes.append(TextNode(content=part))
        
        return nodes


# Global parser instance
_parser = PSXParser()


def psx(psx_str: str, context: Dict[str, Any] = None) -> PSXElement:
    """
    Parse PSX string to PSXElement (legacy interface)
    Automatically captures local variables for expression evaluation
    """
    import inspect
    
    # Only capture locals if no context is provided (not called from component)
    captured_locals = {}
    if context is None:
        try:
            frame = inspect.currentframe().f_back
            if frame:
                # Filter out internal variables
                frame_locals = frame.f_locals
                captured_locals = {
                    k: v for k, v in frame_locals.items()
                    if not k.startswith('_') and 
                       not callable(v) and
                       not hasattr(v, '__call__')
                }
        except Exception:
            pass
    
    # Merge provided context with captured locals
    merged_context = captured_locals.copy()
    if context:
        merged_context.update(context)
    
    # Parse with production-grade parser
    ast_node = _parser.parse_psx(psx_str, merged_context)
    
    # Store the context and AST node in the PSXElement for rendering
    if isinstance(ast_node, ElementNode):
        element = PSXElement(
            tag=ast_node.tag,
            props=ast_node.attributes,
            children=[],
            key=ast_node.key
        )
        # Store the AST node and context for proper rendering
        element._ast_node = ast_node
        element._psx_context = merged_context
        return element
    else:
        # For non-elements, wrap in div
        element = PSXElement(
            tag='div',
            props={},
            children=[str(ast_node)]
        )
        element._ast_node = ast_node
        element._psx_context = merged_context
        return element


def render_psx(element, context: Dict[str, Any] = None) -> str:
    """Render PSX element to HTML string"""
    if isinstance(element, PSXElement):
        return element.to_html(context)
    elif isinstance(element, str):
        return element
    else:
        return str(element)


# Legacy exports
def fragment(children: Any) -> str:
    """Fragment component for multiple children"""
    if isinstance(children, list):
        return ''.join(str(child) for child in children)
    else:
        return str(children)


def key(key_value: str, element: PSXElement) -> PSXElement:
    """Add key to PSX element"""
    element.key = key_value
    return element


# Export all PSX components
__all__ = [
    # Legacy interface
    'PSXElement', 'PSXParser', 'psx', 'render_psx', 
    'fragment', 'key', 'process_python_logic',
    
    # Production-grade interface
    'PSXASTParser', 'PSXNodeValidator', 'PSXNodeOptimizer'
]
