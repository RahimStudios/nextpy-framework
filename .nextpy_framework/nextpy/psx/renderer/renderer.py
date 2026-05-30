"""
PSX Renderer - Production-grade rendering with core integration
"""

from typing import Any, Dict, List
from ..core import PSXRuntime, PSXNodeUnion
from ..core.parser import PSXElement
from ..vdom.vnode import VNode, create_element


class PSXRenderer:
    """Production-grade PSX renderer with core integration"""
    
    def __init__(self):
        self._cache = {}
        self.runtime = PSXRuntime()
    
    def render(self, element: PSXElement, context: Dict[str, Any] = None) -> str:
        """Render PSX element to HTML string using production-grade runtime"""
        context = context or {}
        
        if isinstance(element, str):
            return element
        
        # Use production-grade runtime for rendering
        if context:
            self.runtime.update_context(context)
        
        # Convert PSXElement to AST and render
        ast_node = element.to_ast()
        return self.runtime._render_node(ast_node)
    
    def render_ast(self, ast_node: PSXNodeUnion, context: Dict[str, Any] = None) -> str:
        """Render PSX AST node directly using production-grade runtime"""
        context = context or {}
        
        if context:
            self.runtime.update_context(context)
        
        return self.runtime._render_node(ast_node)
    
    def _psx_to_vnode(self, element: PSXElement, context: Dict[str, Any]) -> VNode:
        """Convert PSXElement to VNode"""
        # Process props
        processed_props = {}
        for key, value in element.props.items():
            if isinstance(value, str) and '{' in value:
                # Evaluate expressions in props
                from ..core.runtime import runtime
                try:
                    processed_props[key] = runtime.evaluator.evaluate(value, context)
                except:
                    processed_props[key] = value
            else:
                processed_props[key] = value
        
        # Process children
        processed_children = []
        for child in element.children:
            if isinstance(child, str):
                processed_children.append(child)
            elif isinstance(child, PSXElement):
                processed_children.append(self._psx_to_vnode(child, context))
        
        return create_element(element.tag, processed_props, processed_children, element.key)
    
    def _vnode_to_html(self, vnode: VNode) -> str:
        """Convert VNode to HTML string"""
        if vnode.type == 'text':
            return vnode.props.get('text', '')
        
        # Build opening tag
        props_str = ''
        if vnode.props:
            prop_parts = []
            for key, value in vnode.props.items():
                if key == 'children' or value is None:
                    continue

                html_key = 'class' if key == 'className' else key
                if isinstance(value, bool):
                    if value:
                        prop_parts.append(f'{html_key}')
                    continue
                if isinstance(value, dict) and html_key == 'style':
                    style_value = '; '.join(f'{k}: {v}' for k, v in value.items())
                    prop_parts.append(f'{html_key}="{style_value}"')
                else:
                    prop_parts.append(f'{html_key}="{value}"')
            props_str = ' ' + ' '.join(prop_parts) if prop_parts else ''
        
        # Handle self-closing tags
        self_closing = {'img', 'br', 'hr', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'}
        
        if vnode.type in self_closing:
            return f'<{vnode.type}{props_str} />'
        
        # Build children
        children_html = ''
        if vnode.children:
            for child in vnode.children:
                if isinstance(child, VNode):
                    children_html += self._vnode_to_html(child)
                else:
                    children_html += str(child)
        
        return f'<{vnode.type}{props_str}>{children_html}</{vnode.type}>'


# Global renderer instance
renderer = PSXRenderer()
