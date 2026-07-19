"""
NextPy Components - Next.js-style component system
Allows writing components exactly like Next.js but in Python
"""

from typing import Any, Dict, List, Union, Optional, Callable
from .jsx import JSXElement, jsx, render_jsx


class Props:
    """Base class for component props"""
    pass


def Component(func):
    """Decorator to create a Next.js-style component"""
    def wrapper(*args, **kwargs):
        # First argument might be props dict
        if args and isinstance(args[0], dict):
            props = args[0]
            return func(props, *args[1:], **kwargs)
        else:
            # No props dict passed
            return func({}, *args, **kwargs)
    
    wrapper.is_component = True
    return wrapper


def Children(props: Dict[str, Any]) -> Any:
    """Access children from props"""
    return props.get('children', [])


# Built-in components
def Head(props: Dict[str, Any]) -> JSXElement:
    """Next.js Head component equivalent"""
    children = props.get('children', [])
    return jsx('head', {}, *children)


def Link(props: Dict[str, Any]) -> JSXElement:
    """Next.js Link component equivalent"""
    href = props.get('href', '#')
    children = props.get('children', [])
    
    return jsx('a', {
        'href': href,
        'onclick': f"window.location.href='{href}'; return false;"
    }, *children)


def Script(props: Dict[str, Any]) -> JSXElement:
    """Next.js Script component equivalent"""
    src = props.get('src')
    children = props.get('children', [])
    
    script_props = {}
    if src:
        script_props['src'] = src
    
    return jsx('script', script_props, *children)


def Image(props: Dict[str, Any]) -> JSXElement:
    """Next.js Image component equivalent"""
    src = props.get('src', '')
    alt = props.get('alt', '')
    width = props.get('width')
    height = props.get('height')
    
    img_props = {'src': src, 'alt': alt}
    if width:
        img_props['width'] = width
    if height:
        img_props['height'] = height
    
    return jsx('img', img_props)


def Meta(props: Dict[str, Any]) -> JSXElement:
    """Next.js Meta component equivalent"""
    return jsx('meta', props)


def Title(props: Dict[str, Any]) -> JSXElement:
    """Next.js Title component equivalent"""
    children = props.get('children', [])
    return jsx('title', {}, *children)


# Layout components
def Layout(props: Dict[str, Any]) -> JSXElement:
    """Basic layout component"""
    children = props.get('children', [])
    title = props.get('title', 'NextPy App')
    
    return jsx('html', {'lang': 'en'},
        jsx('head', {},
            jsx('meta', {'charset': 'utf-8'}),
            jsx('meta', {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}),
            jsx('title', {}, title),
            Meta({'name': 'description', 'content': 'NextPy Application'})
        ),
        jsx('body', {}, *children)
    )


def Container(props: Dict[str, Any]) -> JSXElement:
    """Container component"""
    children = props.get('children', [])
    className = props.get('className', 'container')
    
    return jsx('div', {'className': className}, *children)


def Row(props: Dict[str, Any]) -> JSXElement:
    """Row component"""
    children = props.get('children', [])
    className = props.get('className', 'row')
    
    return jsx('div', {'className': className}, *children)


def Col(props: Dict[str, Any]) -> JSXElement:
    """Column component"""
    children = props.get('children', [])
    className = props.get('className', 'col')
    
    return jsx('div', {'className': className}, *children)


# Form components
def Form(props: Dict[str, Any]) -> JSXElement:
    """Form component"""
    action = props.get('action', '')
    method = props.get('method', 'GET')
    children = props.get('children', [])
    
    return jsx('form', {'action': action, 'method': method}, *children)


def Input(props: Dict[str, Any]) -> JSXElement:
    """Input component"""
    input_type = props.get('type', 'text')
    name = props.get('name', '')
    value = props.get('value', '')
    placeholder = props.get('placeholder', '')
    required = props.get('required', False)
    
    input_props = {
        'type': input_type,
        'name': name,
        'value': value,
        'placeholder': placeholder
    }
    
    if required:
        input_props['required'] = 'required'
    
    return jsx('input', input_props)


def Button(props: Dict[str, Any]) -> JSXElement:
    """Button component"""
    button_type = props.get('type', 'button')
    onclick = props.get('onClick')
    children = props.get('children', [])
    disabled = props.get('disabled', False)
    
    button_props = {'type': button_type}
    
    if onclick and callable(onclick):
        # Convert Python function to JavaScript call
        button_props['onclick'] = f"alert('Button clicked!')"
    
    if disabled:
        button_props['disabled'] = 'disabled'
    
    return jsx('button', button_props, *children)


# Navigation components
def Navbar(props: Dict[str, Any]) -> JSXElement:
    """Navigation bar component"""
    children = props.get('children', [])
    brand = props.get('brand', 'NextPy')
    
    return jsx('nav', {'className': 'navbar'},
        jsx('div', {'className': 'nav-brand'}, brand),
        jsx('div', {'className': 'nav-links'}, *children)
    )


def NavItem(props: Dict[str, Any]) -> JSXElement:
    """Navigation item component"""
    href = props.get('href', '#')
    children = props.get('children', [])
    
    return Link({'href': href}, *children)


# Card components
def Card(props: Dict[str, Any]) -> JSXElement:
    """Card component"""
    children = props.get('children', [])
    title = props.get('title')
    footer = props.get('footer')
    
    card_content = []
    
    if title:
        card_content.append(jsx('div', {'className': 'card-header'},
            jsx('h3', {}, title)
        ))
    
    card_content.append(jsx('div', {'className': 'card-body'}, *children))
    
    if footer:
        card_content.append(jsx('div', {'className': 'card-footer'}, footer))
    
    return jsx('div', {'className': 'card'}, *card_content)


# List components
def List(props: Dict[str, Any]) -> JSXElement:
    """List component"""
    items = props.get('items', [])
    ordered = props.get('ordered', False)
    
    tag = 'ol' if ordered else 'ul'
    
    list_items = []
    for item in items:
        if isinstance(item, dict):
            list_items.append(jsx('li', {}, item.get('text', str(item))))
        else:
            list_items.append(jsx('li', {}, str(item)))
    
    return jsx(tag, {}, *list_items)


# Utility components
def Conditional(props: Dict[str, Any]) -> JSXElement:
    """Conditional rendering component"""
    condition = props.get('condition', True)
    children = props.get('children', [])
    
    if condition:
        return jsx('fragment', {}, *children)
    else:
        return jsx('fragment', {})


def Loop(props: Dict[str, Any]) -> JSXElement:
    """Loop rendering component"""
    items = props.get('items', [])
    render_func = props.get('render')
    
    if not render_func or not callable(render_func):
        return jsx('fragment', {})
    
    elements = []
    for item in items:
        elements.append(render_func(item))
    
    return jsx('fragment', {}, *elements)


# Error boundary component
def ErrorBoundary(props: Dict[str, Any]) -> JSXElement:
    """Error boundary component"""
    children = props.get('children', [])
    fallback = props.get('fallback', jsx('div', {}, 'Something went wrong'))
    
    # In a real implementation, this would catch errors
    # For now, just render children
    return jsx('fragment', {}, *children)


# Suspense component
def Suspense(props: Dict[str, Any]) -> JSXElement:
    """Suspense component for lazy loading"""
    children = props.get('children', [])
    fallback = props.get('fallback', jsx('div', {}, 'Loading...'))
    
    # In a real implementation, this would handle async components
    # For now, just render children
    return jsx('fragment', {}, *children)
