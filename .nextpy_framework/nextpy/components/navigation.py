"""
Navigation Components for NextPy - Updated for JSX system
Navigation, menu, and related components
"""

from typing import Optional, List, Dict, Any, Union
from ..jsx import div, ul, li, a, span, button, nav, header, img, input


def Navbar(
    brand: str = "",
    brand_href: str = "/",
    logo: str = "",
    menu_items: List[Dict[str, str]] = None,
    variant: str = "default",
    sticky: bool = False,
    class_name: str = "",
    **kwargs
):
    """Navbar component - returns JSX element"""
    if menu_items is None:
        menu_items = []
    
    # Base classes
    base_class = "bg-white shadow-sm"
    sticky_class = "sticky top-0 z-50" if sticky else ""
    
    # Variant classes
    variants = {
        "default": "bg-white shadow-sm",
        "dark": "bg-gray-800 text-white",
        "transparent": "bg-transparent absolute top-0 w-full"
    }
    
    navbar_class = f"{variants.get(variant, variants['default'])} {sticky_class}"
    
    # Brand section
    brand_content = []
    if logo:
        brand_content.append(img({'src': logo, 'alt': brand, 'className': 'h-8 w-auto mr-2'}))
    if brand:
        brand_content.append(a({'href': brand_href, 'className': 'text-xl font-bold text-gray-900 hover:text-gray-700'}, brand))
    
    # Menu items
    menu_content = []
    for item in menu_items:
        item_class = "text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
        if variant == "dark":
            item_class = "text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
        
        menu_content.append(li({}, a({'href': item.get('href', '#'), 'className': item_class}, item.get('label', ''))))
    
    return header({'className': f"{navbar_class} {class_name}".strip()},
              div({'className': 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'},
                  div({'className': 'flex justify-between items-center h-16'},
                      # Brand
                      div({'className': 'flex items-center'}, *brand_content),
                      
                      # Navigation menu
                      nav({'className': 'hidden md:flex space-x-8'},
                          ul({'className': 'flex space-x-4'}, *menu_content)
                      ),
                      
                      # Mobile menu button
                      button({'className': 'md:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100'}, '☰')
                  )
              )
    )


def Sidebar(
    menu_items: List[Dict[str, str]] = None,
    position: str = "left",
    width: str = "w-64",
    variant: str = "default",
    class_name: str = "",
    **kwargs
):
    """Sidebar component - returns JSX element"""
    if menu_items is None:
        menu_items = []
    
    # Base classes
    base_class = "bg-white shadow-lg"
    
    # Variant classes
    variants = {
        "default": "bg-white shadow-lg",
        "dark": "bg-gray-800 text-white",
        "bordered": "bg-white border-r border-gray-200"
    }
    
    sidebar_class = f"{variants.get(variant, variants['default'])} {width}"
    
    # Menu items
    menu_content = []
    for item in menu_items:
        item_class = "block px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
        if variant == "dark":
            item_class = "block px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700"
        
        # Add icon if present
        item_content = []
        if item.get('icon'):
            item_content.append(span({'className': 'mr-3'}, item.get('icon')))
        item_content.append(item.get('label', ''))
        
        menu_content.append(li({}, a({'href': item.get('href', '#'), 'className': item_class}, *item_content)))
    
    return div({'className': f"{sidebar_class} {class_name}".strip()},
              div({'className': 'p-4'},
                  h3({'className': 'text-lg font-semibold text-gray-900 mb-4'}, 'Navigation'),
                  ul({'className': 'space-y-1'}, *menu_content)
              )
    )


def Menu(
    items: List[Dict[str, str]] = None,
    variant: str = "vertical",
    class_name: str = "",
    **kwargs
):
    """Menu component - returns JSX element"""
    if items is None:
        items = []
    
    # Base classes
    base_class = "bg-white rounded-lg shadow-md border border-gray-200"
    
    # Direction classes
    directions = {
        "vertical": "flex-col",
        "horizontal": "flex-row"
    }
    
    menu_class = f"{base_class} {directions.get(variant, directions['vertical'])}"
    
    # Menu items
    menu_content = []
    for item in items:
        item_class = "block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
        if variant == "horizontal":
            item_class = "block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 border-r border-gray-200 last:border-r-0"
        
        menu_content.append(li({}, a({'href': item.get('href', '#'), 'className': item_class}, item.get('label', ''))))
    
    return ul({'className': f"{menu_class} {class_name}".strip()}, *menu_content)


def Dropdown(
    trigger: str = "Menu",
    items: List[Dict[str, str]] = None,
    position: str = "bottom-left",
    variant: str = "default",
    class_name: str = "",
    **kwargs
):
    """Dropdown component - returns JSX element"""
    if items is None:
        items = []
    
    # Position classes
    positions = {
        "bottom-left": "left-0 top-full mt-1",
        "bottom-right": "right-0 top-full mt-1",
        "top-left": "left-0 bottom-full mb-1",
        "top-right": "right-0 bottom-full mb-1"
    }
    
    # Base classes
    trigger_class = "inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
    menu_class = f"absolute z-10 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 {positions.get(position, positions['bottom-left'])}"
    
    # Dropdown items
    dropdown_content = []
    for item in items:
        item_class = "block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
        if item.get('separator'):
            dropdown_content.append(li({'className': 'border-t border-gray-100'}))
        else:
            dropdown_content.append(li({}, a({'href': item.get('href', '#'), 'className': item_class}, item.get('label', ''))))
    
    return div({'className': f'relative inline-block text-left {class_name}'.strip()},
              button({'className': trigger_class}, trigger, span({'className': 'ml-2'}, '▼')),
              div({'className': menu_class},
                  div({'className': 'py-1'}, *dropdown_content)
              )
    )


def Tabs(
    tabs: List[Dict[str, str]] = None,
    active_tab: str = "",
    variant: str = "default",
    class_name: str = "",
    **kwargs
):
    """Tabs component - returns JSX element"""
    if tabs is None:
        tabs = []
    
    # Base classes
    base_class = "border-b border-gray-200"
    
    # Variant classes
    variants = {
        "default": "border-b border-gray-200",
        "pills": "space-x-2",
        "underline": "border-b-2 border-transparent"
    }
    
    tabs_class = f"{variants.get(variant, variants['default'])}"
    
    # Tab items
    tab_content = []
    for tab in tabs:
        tab_id = tab.get('id', tab.get('label', '').lower().replace(' ', '-'))
        is_active = tab_id == active_tab
        
        if variant == "pills":
            tab_class = "px-3 py-2 text-sm font-medium rounded-md"
            if is_active:
                tab_class += " bg-blue-100 text-blue-700"
            else:
                tab_class += " text-gray-500 hover:text-gray-700"
        elif variant == "underline":
            tab_class = "py-2 px-1 border-b-2 font-medium text-sm"
            if is_active:
                tab_class += " border-blue-500 text-blue-600"
            else:
                tab_class += " border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
        else:
            tab_class = "py-2 px-1 border-b-2 font-medium text-sm"
            if is_active:
                tab_class += " border-blue-500 text-blue-600"
            else:
                tab_class += " border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
        
        tab_content.append(li({}, a({'href': tab.get('href', '#'), 'className': tab_class}, tab.get('label', ''))))
    
    return nav({'className': f"{tabs_class} {class_name}".strip()},
              ul({'className': f'flex {"-mb-px" if variant != "pills" else ""}'}, *tab_content)
    )


def Pagination(
    current_page: int = 1,
    total_pages: int = 10,
    href_template: str = "?page={}",
    variant: str = "default",
    class_name: str = "",
    **kwargs
):
    """Pagination component - returns JSX element"""
    
    # Base classes
    base_class = "flex items-center justify-between"
    
    # Variant classes
    variants = {
        "default": "space-x-2",
        "centered": "justify-center space-x-2",
        "simple": "space-x-2"
    }
    
    pagination_class = f"{base_class} {variants.get(variant, variants['default'])}"
    
    content = []
    
    # Previous button
    prev_disabled = current_page <= 1
    prev_class = "px-3 py-1 text-sm border border-gray-300 rounded-md"
    if prev_disabled:
        prev_class += " opacity-50 cursor-not-allowed"
    else:
        prev_class += " hover:bg-gray-50"
    
    content.append(button({
        'className': prev_class,
        'disabled': prev_disabled,
        'href': href_template.format(current_page - 1) if not prev_disabled else '#'
    }, 'Previous'))
    
    # Page numbers
    if variant != "simple":
        start_page = max(1, current_page - 2)
        end_page = min(total_pages, current_page + 2)
        
        if start_page > 1:
            content.append(button({'className': 'px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50'}, '1'))
            if start_page > 2:
                content.append(span({'className': 'px-2'}, '...'))
        
        for page in range(start_page, end_page + 1):
            is_active = page == current_page
            page_class = "px-3 py-1 text-sm border rounded-md"
            if is_active:
                page_class += " bg-blue-500 text-white border-blue-500"
            else:
                page_class += " border-gray-300 hover:bg-gray-50"
            
            content.append(button({
                'className': page_class,
                'href': href_template.format(page)
            }, str(page)))
        
        if end_page < total_pages:
            if end_page < total_pages - 1:
                content.append(span({'className': 'px-2'}, '...'))
            content.append(button({'className': 'px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50'}, str(total_pages)))
    
    # Next button
    next_disabled = current_page >= total_pages
    next_class = "px-3 py-1 text-sm border border-gray-300 rounded-md"
    if next_disabled:
        next_class += " opacity-50 cursor-not-allowed"
    else:
        next_class += " hover:bg-gray-50"
    
    content.append(button({
        'className': next_class,
        'disabled': next_disabled,
        'href': href_template.format(current_page + 1) if not next_disabled else '#'
    }, 'Next'))
    
    return nav({'className': f"{pagination_class} {class_name}".strip()}, *content)


def SearchBar(
    placeholder: str = "Search...",
    value: str = "",
    on_search: str = "",
    variant: str = "default",
    class_name: str = "",
    **kwargs
):
    """SearchBar component - returns JSX element"""
    
    # Base classes
    base_class = "relative"
    
    # Variant classes
    variants = {
        "default": "max-w-md",
        "full": "w-full",
        "compact": "max-w-xs"
    }
    
    search_class = f"{base_class} {variants.get(variant, variants['default'])}"
    
    input_class = "block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
    
    return div({'className': f"{search_class} {class_name}".strip()},
              div({'className': 'absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none'},
                  span({'className': 'text-gray-400 sm:text-sm'}, '🔍')
              ),
              input({
                  'type': 'text',
                  'value': value,
                  'placeholder': placeholder,
                  'className': input_class,
                  'onKeyDown': on_search
              })
    )


def BreadcrumbNav(
    items: List[Dict[str, str]] = None,
    separator: str = "/",
    class_name: str = "",
    **kwargs
):
    """BreadcrumbNav component - returns JSX element"""
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
    
    return nav({'className': f"aria-label='Breadcrumb' {base_class} {class_name}".strip()}, *content)
