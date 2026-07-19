"""
Layout components for NextPy - Updated for JSX system
Provides grid, flex, container, and other layout utilities
"""

from typing import Optional, List, Dict, Any, Union
from ..jsx import div, section, article, aside, header, footer, main, nav


def Container(
    children: List = None,
    max_width: str = "max-w-6xl",
    padding: str = "px-4 sm:px-6 lg:px-8",
    class_name: str = "",
    **kwargs
):
    """Container component with responsive max-width - returns JSX element"""
    if children is None:
        children = []
    
    classes = f"mx-auto {max_width} {padding}"
    return div({'className': f"{classes} {class_name}".strip()}, *children)


def Grid(
    children: List = None,
    columns: int = 3,
    gap: str = "gap-6",
    responsive: bool = True,
    class_name: str = "",
    **kwargs
):
    """Grid layout component - returns JSX element"""
    if children is None:
        children = []
    
    if responsive:
        cols = f"md:grid-cols-{columns}"
        classes = f"grid {cols} {gap}"
    else:
        cols = f"grid-cols-{columns}"
        classes = f"grid {cols} {gap}"
    
    return div({'className': f"{classes} {class_name}".strip()}, *children)


def Flex(
    children: List = [],
    direction: str = "row",
    justify: str = "justify-start",
    align: str = "items-start",
    gap: str = "gap-4",
    wrap: bool = False,
    class_name: str = "",
    **kwargs
):
    """Flex layout component - returns JSX element"""
    if children is None:
        children = []
    
    flex_dir = "flex-col" if direction == "column" else "flex-row"
    wrap_class = "flex-wrap" if wrap else ""
    classes = f"flex {flex_dir} {justify} {align} {gap} {wrap_class}"
    
    return div({'className': f"{classes} {class_name}".strip()}, *children)


def Stack(
    children: List = None,
    direction: str = "vertical",
    spacing: str = "space-y-4",
    class_name: str = "",
    **kwargs
):
    """Stack component - returns JSX element"""
    if children is None:
        children = []
    
    if direction == "horizontal":
        spacing_class = spacing.replace('space-y', 'space-x')
    else:
        spacing_class = spacing
    
    return div({'className': f"{spacing_class} {class_name}".strip()}, *children)


def Sidebar(
    children: List = None,
    position: str = "left",
    width: str = "w-64",
    class_name: str = "",
    **kwargs
):
    """Sidebar component - returns JSX element"""
    if children is None:
        children = []
    
    position_class = "order-first" if position == "left" else "order-last"
    classes = f"{width} {position_class}"
    
    return aside({'className': f"{classes} {class_name}".strip()}, *children)


def MainContent(
    children: List = None,
    class_name: str = "",
    **kwargs
):
    """Main content component - returns JSX element"""
    if children is None:
        children = []
    
    default_class = "flex-1 min-w-0"
    return main({'className': f"{default_class} {class_name}".strip()}, *children)


def Section(
    children: List = None,
    class_name: str = "",
    id: str = "",
    **kwargs
):
    """Section component - returns JSX element"""
    if children is None:
        children = []
    
    props = {'className': class_name}
    if id:
        props['id'] = id
    
    return section(props, *children)


def Article(
    children: List = None,
    class_name: str = "",
    **kwargs
):
    """Article component - returns JSX element"""
    if children is None:
        children = []
    
    return article({'className': class_name}, *children)


def Header(
    children: List = None,
    class_name: str = "",
    sticky: bool = False,
    **kwargs
):
    """Header component - returns JSX element"""
    if children is None:
        children = []
    
    sticky_class = "sticky top-0 z-50" if sticky else ""
    default_class = "bg-white shadow-sm"
    classes = f"{default_class} {sticky_class}"
    
    return header({'className': f"{classes} {class_name}".strip()}, *children)


def Footer(
    children: List = None,
    class_name: str = "",
    **kwargs
):
    """Footer component - returns JSX element"""
    if children is None:
        children = []
    
    default_class = "bg-gray-100 border-t border-gray-200"
    return footer({'className': f"{default_class} {class_name}".strip()}, *children)


def Navigation(
    children: List = None,
    class_name: str = "",
    **kwargs
):
    """Navigation component - returns JSX element"""
    if children is None:
        children = []
    
    default_class = "flex space-x-8"
    return nav({'className': f"{default_class} {class_name}".strip()}, *children)


def Center(
    children: List = None,
    class_name: str = "",
    **kwargs
):
    """Center component - returns JSX element"""
    if children is None:
        children = []
    
    default_class = "flex items-center justify-center"
    return div({'className': f"{default_class} {class_name}".strip()}, *children)


def Spacer(
    size: str = "medium",
    class_name: str = "",
    **kwargs
):
    """Spacer component - returns JSX element"""
    size_classes = {
        "small": "h-2",
        "medium": "h-4",
        "large": "h-8",
        "xlarge": "h-16"
    }
    
    spacer_class = size_classes.get(size, "h-4")
    return div({'className': f"{spacer_class} {class_name}".strip()})


def Divider(
    orientation: str = "horizontal",
    class_name: str = "",
    **kwargs
):
    """Divider component - returns JSX element"""
    if orientation == "vertical":
        default_class = "w-px h-6 bg-gray-300"
    else:
        default_class = "h-px w-full bg-gray-300"
    
    return div({'className': f"{default_class} {class_name}".strip()})


def AspectRatio(
    children: List = None,
    ratio: str = "16/9",
    class_name: str = "",
    **kwargs
):
    """AspectRatio component - returns JSX element"""
    if children is None:
        children = []
    
    # Convert ratio to percentage
    if '/' in ratio:
        numerator, denominator = ratio.split('/')
        percentage = (int(denominator) / int(numerator)) * 100
    else:
        percentage = 56.25  # Default 16:9
    
    style = f"position: relative; padding-bottom: {percentage}%;"
    inner_style = "position: absolute; top: 0; left: 0; right: 0; bottom: 0;"
    
    return div({'className': class_name, 'style': style},
        div({'style': inner_style}, *children)
    )


def Card(
    children: List = None,
    title: str = "",
    subtitle: str = "",
    footer: str = "",
    class_name: str = "",
    **kwargs
):
    """Card component - returns JSX element"""
    if children is None:
        children = []
    
    default_class = "bg-white rounded-lg shadow-md border border-gray-200"
    
    content = []
    
    if title or subtitle:
        header_content = []
        if title:
            header_content.append(div({'className': 'text-lg font-semibold text-gray-900'}, title))
        if subtitle:
            header_content.append(div({'className': 'text-sm text-gray-600'}, subtitle))
        
        content.append(div({'className': 'p-6 pb-4'}, *header_content))
    
    if children:
        content.append(div({'className': 'p-6 pt-0'}, *children))
    
    if footer:
        content.append(div({'className': 'p-6 pt-0 border-t border-gray-200'}, footer))
    
    return div({'className': f"{default_class} {class_name}".strip()}, *content)
