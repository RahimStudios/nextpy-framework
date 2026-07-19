"""
UI Components for NextPy - Updated for JSX system
Common UI components for rapid development
"""

from typing import Optional, List, Dict, Any, Union
from ..jsx import div, span, p, h1, h2, h3, h4, h5, h6, button, a, img, ul, ol, li, table, thead, tbody, tr, th, td, strong, em, code, pre, blockquote


def Button(
    text: str = "",
    variant: str = "primary",
    size: str = "medium",
    disabled: bool = False,
    loading: bool = False,
    icon: str = "",
    href: str = "",
    onclick: str = "",
    class_name: str = "",
    **kwargs
):
    """Button component - returns JSX element"""
    
    # Base classes
    base_class = "inline-flex items-center justify-center font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2"
    
    # Variant classes
    variants = {
        "primary": "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
        "secondary": "bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500",
        "success": "bg-green-600 text-white hover:bg-green-700 focus:ring-green-500",
        "warning": "bg-yellow-600 text-white hover:bg-yellow-700 focus:ring-yellow-500",
        "danger": "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
        "outline": "border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 focus:ring-blue-500",
        "ghost": "text-gray-700 hover:bg-gray-100 focus:ring-gray-500"
    }
    
    # Size classes
    sizes = {
        "small": "px-3 py-1.5 text-sm",
        "medium": "px-4 py-2 text-sm",
        "large": "px-6 py-3 text-base"
    }
    
    classes = f"{base_class} {variants.get(variant, variants['primary'])} {sizes.get(size, sizes['medium'])}"
    if disabled or loading:
        classes += " opacity-50 cursor-not-allowed"
    
    props = {
        'className': f"{classes} {class_name}".strip()
    }
    
    if disabled or loading:
        props['disabled'] = True
    if onclick:
        props['onClick'] = onclick
    
    # Content
    content = []
    if loading:
        content.append(span({'className': 'mr-2'}, '⏳'))
    elif icon:
        content.append(span({'className': 'mr-2'}, icon))
    
    content.append(text or 'Button')
    
    if href:
        return a({'href': href, **props}, *content)
    else:
        return button(props, *content)


def Badge(
    text: str = "",
    variant: str = "primary",
    size: str = "medium",
    class_name: str = "",
    **kwargs
):
    """Badge component - returns JSX element"""
    
    # Base classes
    base_class = "inline-flex items-center font-medium rounded-full"
    
    # Variant classes
    variants = {
        "primary": "bg-blue-100 text-blue-800",
        "secondary": "bg-gray-100 text-gray-800",
        "success": "bg-green-100 text-green-800",
        "warning": "bg-yellow-100 text-yellow-800",
        "danger": "bg-red-100 text-red-800",
        "info": "bg-blue-100 text-blue-800"
    }
    
    # Size classes
    sizes = {
        "small": "px-2 py-0.5 text-xs",
        "medium": "px-2.5 py-0.5 text-sm",
        "large": "px-3 py-1 text-sm"
    }
    
    classes = f"{base_class} {variants.get(variant, variants['primary'])} {sizes.get(size, sizes['medium'])}"
    
    return span({'className': f"{classes} {class_name}".strip()}, text)


def Avatar(
    src: str = "",
    alt: str = "",
    size: str = "medium",
    fallback: str = "",
    class_name: str = "",
    **kwargs
):
    """Avatar component - returns JSX element"""
    
    # Size classes
    sizes = {
        "small": "h-6 w-6",
        "medium": "h-8 w-8",
        "large": "h-10 w-10",
        "xlarge": "h-12 w-12"
    }
    
    base_class = f"rounded-full object-cover {sizes.get(size, sizes['medium'])}"
    
    if src:
        return img({'src': src, 'alt': alt, 'className': f"{base_class} {class_name}".strip()})
    else:
        # Fallback avatar with initials
        fallback_class = f"rounded-full bg-gray-300 flex items-center justify-center text-gray-600 font-medium {sizes.get(size, sizes['medium'])}"
        return div({'className': f"{fallback_class} {class_name}".strip()}, 
                  span({'className': 'text-sm'}, fallback[:2].upper()))


def Icon(
    name: str = "",
    size: str = "medium",
    class_name: str = "",
    **kwargs
):
    """Icon component - returns JSX element"""
    
    # Size classes
    sizes = {
        "small": "w-4 h-4",
        "medium": "w-5 h-5",
        "large": "w-6 h-6",
        "xlarge": "w-8 h-8"
    }
    
    # Simple icon mapping (you can expand this)
    icons = {
        "home": "🏠",
        "user": "👤",
        "settings": "⚙️",
        "search": "🔍",
        "heart": "❤️",
        "star": "⭐",
        "check": "✓",
        "close": "✕",
        "menu": "☰",
        "arrow-right": "→",
        "arrow-left": "←",
        "arrow-up": "↑",
        "arrow-down": "↓"
    }
    
    icon_char = icons.get(name, "•")
    size_class = sizes.get(size, sizes['medium'])
    
    return span({'className': f"{size_class} {class_name}".strip()}, icon_char)


def Alert(
    message: str = "",
    variant: str = "info",
    dismissible: bool = False,
    class_name: str = "",
    **kwargs
):
    """Alert component - returns JSX element"""
    
    # Base classes
    base_class = "p-4 rounded-md border"
    
    # Variant classes
    variants = {
        "info": "bg-blue-50 border-blue-200 text-blue-800",
        "success": "bg-green-50 border-green-200 text-green-800",
        "warning": "bg-yellow-50 border-yellow-200 text-yellow-800",
        "error": "bg-red-50 border-red-200 text-red-800"
    }
    
    classes = f"{base_class} {variants.get(variant, variants['info'])}"
    
    content = [div({'className': 'font-medium'}, message)]
    
    if dismissible:
        content.append(button({'className': 'ml-auto -mr-1.5 -mt-1.5 p-1.5 rounded-md hover:bg-opacity-20'}, '✕'))
    
    return div({'className': f"{classes} {class_name}".strip()}, 
              div({'className': 'flex'}, *content))


def Progress(
    value: int = 0,
    max: int = 100,
    variant: str = "primary",
    size: str = "medium",
    show_label: bool = True,
    class_name: str = "",
    **kwargs
):
    """Progress component - returns JSX element"""
    
    # Base classes
    base_class = "w-full bg-gray-200 rounded-full"
    
    # Size classes
    sizes = {
        "small": "h-1",
        "medium": "h-2",
        "large": "h-3"
    }
    
    # Variant classes for progress bar
    variants = {
        "primary": "bg-blue-600",
        "success": "bg-green-600",
        "warning": "bg-yellow-600",
        "error": "bg-red-600"
    }
    
    container_class = f"{base_class} {sizes.get(size, sizes['medium'])}"
    bar_class = f"{variants.get(variant, variants['primary'])} {sizes.get(size, sizes['medium'])} rounded-full transition-all duration-300"
    
    percentage = min(100, max(0, (value / max) * 100))
    
    content = [
        div({'className': container_class},
             div({'className': bar_class, 'style': f'width: {percentage}%'}))
    ]
    
    if show_label:
        content.append(p({'className': 'text-sm text-gray-600 mt-1'}, f'{value}/{max}'))
    
    return div({'className': class_name}, *content)


def Skeleton(
    variant: str = "text",
    width: str = "w-full",
    height: str = "h-4",
    class_name: str = "",
    **kwargs
):
    """Skeleton component - returns JSX element"""
    
    base_class = "animate-pulse bg-gray-300 rounded"
    
    # Variant-specific classes
    variants = {
        "text": "h-4",
        "heading": "h-8",
        "paragraph": "h-4",
        "avatar": "h-10 w-10 rounded-full",
        "button": "h-10 w-20 rounded-md",
        "card": "h-32"
    }
    
    variant_class = variants.get(variant, variants['text'])
    classes = f"{base_class} {variant_class} {width} {height}"
    
    return div({'className': f"{classes} {class_name}".strip()})


def Tooltip(
    text: str = "",
    position: str = "top",
    children: List = None,
    class_name: str = "",
    **kwargs
):
    """Tooltip component - returns JSX element"""
    if children is None:
        children = []
    
    # Position classes
    positions = {
        "top": "bottom-full left-1/2 transform -translate-x-1/2 mb-2",
        "bottom": "top-full left-1/2 transform -translate-x-1/2 mt-2",
        "left": "right-full top-1/2 transform -translate-y-1/2 mr-2",
        "right": "left-full top-1/2 transform -translate-y-1/2 ml-2"
    }
    
    tooltip_class = f"absolute bg-gray-800 text-white text-xs rounded px-2 py-1 whitespace-nowrap {positions.get(position, positions['top'])}"
    
    return div({'className': 'relative inline-block'},
              *children,
              span({'className': tooltip_class}, text)
    )


def Chip(
    text: str = "",
    variant: str = "default",
    removable: bool = False,
    on_remove: str = "",
    class_name: str = "",
    **kwargs
):
    """Chip component - returns JSX element"""
    
    # Base classes
    base_class = "inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
    
    # Variant classes
    variants = {
        "default": "bg-gray-100 text-gray-800",
        "primary": "bg-blue-100 text-blue-800",
        "secondary": "bg-purple-100 text-purple-800",
        "success": "bg-green-100 text-green-800",
        "warning": "bg-yellow-100 text-yellow-800",
        "danger": "bg-red-100 text-red-800"
    }
    
    classes = f"{base_class} {variants.get(variant, variants['default'])}"
    
    content = [text]
    
    if removable:
        remove_button = button({
            'className': 'ml-1 text-gray-600 hover:text-gray-800',
            'onClick': on_remove
        }, '✕')
        content.append(remove_button)
    
    return div({'className': f"{classes} {class_name}".strip()}, *content)


def Breadcrumb(
    items: List[Dict[str, str]] = None,
    separator: str = "/",
    class_name: str = "",
    **kwargs
):
    """Breadcrumb component - returns JSX element"""
    if items is None:
        items = []
    
    base_class = "flex items-center space-x-2 text-sm"
    
    content = []
    
    for i, item in enumerate(items):
        if i > 0:
            content.append(span({'className': 'text-gray-400'}, separator))
        
        if i == len(items) - 1:
            # Last item - not a link
            content.append(span({'className': 'text-gray-900 font-medium'}, item.get('label', '')))
        else:
            # Link item
            content.append(a({'href': item.get('href', '#'), 'className': 'text-gray-600 hover:text-gray-900'}, 
                           item.get('label', '')))
    
    return nav({'className': f"{base_class} {class_name}".strip()}, *content)


def Table(
    headers: List[str] = None,
    rows: List[List[str]] = None,
    variant: str = "default",
    class_name: str = "",
    **kwargs
):
    """Table component - returns JSX element"""
    if headers is None:
        headers = []
    if rows is None:
        rows = []
    
    # Base classes
    base_class = "min-w-full divide-y divide-gray-200"
    
    # Variant classes
    variants = {
        "default": "bg-white",
        "striped": "bg-white",
        "bordered": "bg-white border border-gray-200"
    }
    
    table_class = f"{base_class} {variants.get(variant, variants['default'])}"
    
    # Header
    header_content = []
    for header in headers:
        header_content.append(th({'className': 'px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'}, header))
    
    # Rows
    row_content = []
    for i, row in enumerate(rows):
        row_classes = []
        if variant == "striped" and i % 2 == 1:
            row_classes.append("bg-gray-50")
        
        cells = []
        for cell in row:
            cells.append(td({'className': 'px-6 py-4 whitespace-nowrap text-sm text-gray-900'}, cell))
        
        row_content.append(tr({'className': ' '.join(row_classes)}, *cells))
    
    return table({'className': f"{table_class} {class_name}".strip()},
               thead({'className': 'bg-gray-50'}, tr({}, *header_content)),
               tbody({}, *row_content)
    )


def Code(
    text: str = "",
    variant: str = "inline",
    language: str = "",
    class_name: str = "",
    **kwargs
):
    """Code component - returns JSX element"""
    
    if variant == "inline":
        return code({'className': f"bg-gray-100 px-1 py-0.5 rounded text-sm font-mono text-gray-800 {class_name}".strip()}, text)
    else:
        # Block code
        base_class = "bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto font-mono text-sm"
        return pre({'className': f"{base_class} {class_name}".strip()}, code({}, text))


def Blockquote(
    text: str = "",
    author: str = "",
    variant: str = "default",
    class_name: str = "",
    **kwargs
):
    """Blockquote component - returns JSX element"""
    
    # Base classes
    base_class = "border-l-4 pl-4 italic"
    
    # Variant classes
    variants = {
        "default": "border-gray-300",
        "primary": "border-blue-500",
        "success": "border-green-500",
        "warning": "border-yellow-500",
        "error": "border-red-500"
    }
    
    classes = f"{base_class} {variants.get(variant, variants['default'])}"
    
    content = [p({'className': 'text-gray-700'}, text)]
    
    if author:
        content.append(p({'className': 'text-sm text-gray-600 mt-2'}, f'— {author}'))
    
    return blockquote({'className': f"{classes} {class_name}".strip()}, *content)
