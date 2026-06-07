"""
NextPy - The Python Web Framdwork
File-based routing, SSR, SSG, and more with FastAPI + PSX (True JSX)
"""

__version__ = "3.7.2"

from nextpy.core.router import Router, Route, DynamicRoute
from nextpy.core.renderer import Renderer
from nextpy.core.data_fetching import (
    get_server_side_props,
    get_static_props,
    get_static_paths,
)
from nextpy.components.head import Head
from nextpy.components.link import Link
from nextpy.server.app import create_app

# Import all PSX features for easy access
from nextpy.psx import (
    # Core PSX
    PSXElement, PSXParser, psx, render_psx, fragment, key,
    process_python_logic, runtime, SafeExpressionEngine,
    
    # VDOM
    VNode, create_element, render, update, get_vdom_metrics,
    
    # Renderer
    PSXRenderer, renderer, render_psx_component,
    
    # Components
    PSXComponent, component, class_component, ChildrenComponent,
    register_component, clsx,
    
    # React Hooks
    useState, useEffect, useContext, useReducer, useRef,
    useMemo, useCallback, useImperativeHandle, useLayoutEffect,
    useDebugValue, useTransition, useDeferredValue, useId,
    
    # Custom Hooks
    useCounter, useToggle, useLocalStorage, useFetch, useDebounce,
    useInterval, usePrevious, useAsync, useMediaQuery, useGeolocation, usePerformance,
    
    # Event Handlers
    create_onclick, create_ondblclick, create_onmousedown, create_onmouseup,
    create_onmouseover, create_onmouseout, create_onmouseenter, create_onmouseleave, create_onmousemove,
    create_onchange, create_onsubmit, create_onreset, create_onfocus, create_onblur,
    create_oninput, create_oninvalid, create_onselect,
    create_onkeydown, create_onkeyup, create_onkeypress,
    create_ontouchstart, create_ontouchend, create_ontouchmove, create_ontouchcancel,
    create_onload, create_onunload, create_onresize, create_onscroll,
    create_ondrag, create_ondragstart, create_ondragend, create_ondragenter,
    create_ondragleave, create_ondragover, create_ondrop,
    create_onplay, create_onpause, create_onended, create_onvolumechange,
    create_ontimeupdate, create_onseeking, create_onseeked,
    create_onloadstart, create_onprogress, create_onerror, create_onabort,
    create_onanimationstart, create_onanimationend, create_onanimationiteration,
    create_ontransitionend, create_ontransitionrun, create_ontransitionstart,
    create_onwheel, create_oncopy, create_oncut, create_onpaste,
    create_onbeforeprint, create_onafterprint, create_onstorage,
    create_onopen, create_onmessage, create_onclose, create_oninstall, create_onactivate,
    
    # Utils
    compile_psx, compile_psx_file, is_psx_file, PSXCompiler,
)

# Legacy hooks for backward compatibility
from nextpy.hooks import (
    useState as legacy_useState,
    useEffect as legacy_useEffect,
    useContext as legacy_useContext,
    useReducer as legacy_useReducer,
    useCallback as legacy_useCallback,
    useMemo as legacy_useMemo,
    useRef as legacy_useRef,
    useCounter as legacy_useCounter,
    useToggle as legacy_useToggle,
    useLocalStorage as legacy_useLocalStorage,
    useFetch as legacy_useFetch,
    useDebounce as legacy_useDebounce,
)

# Export everything for easy access
__all__ = [
    # Core NextPy
    'Router', 'Route', 'DynamicRoute', 'Renderer', 'create_app',
    'get_server_side_props', 'get_static_props', 'get_static_paths',
    'Head', 'Link',
    
    # PSX Core
    'PSXElement', 'PSXParser', 'psx', 'render_psx', 'fragment', 'key',
    'process_python_logic', 'runtime', 'SafeExpressionEngine',
    
    # PSX VDOM
    'VNode', 'create_element', 'render', 'update', 'get_vdom_metrics',
    
    # PSX Renderer
    'PSXRenderer', 'renderer', 'render_psx_component',
    
    # PSX Components
    'PSXComponent', 'component', 'class_component', 'ChildrenComponent',
    'register_component', 'clsx',
    
    # PSX React Hooks
    'useState', 'useEffect', 'useContext', 'useReducer', 'useRef',
    'useMemo', 'useCallback', 'useImperativeHandle', 'useLayoutEffect',
    'useDebugValue', 'useTransition', 'useDeferredValue', 'useId',
    
    # PSX Custom Hooks
    'useCounter', 'useToggle', 'useLocalStorage', 'useFetch', 'useDebounce',
    'useInterval', 'usePrevious', 'useAsync', 'useMediaQuery', 'useGeolocation', 'usePerformance',
    
    # PSX Event Handlers
    'create_onclick', 'create_ondblclick', 'create_onmousedown', 'create_onmouseup',
    'create_onmouseover', 'create_onmouseout', 'create_onmouseenter', 'create_onmouseleave', 'create_onmousemove',
    'create_onchange', 'create_onsubmit', 'create_onreset', 'create_onfocus', 'create_onblur',
    'create_oninput', 'create_oninvalid', 'create_onselect',
    'create_onkeydown', 'create_onkeyup', 'create_onkeypress',
    'create_ontouchstart', 'create_ontouchend', 'create_ontouchmove', 'create_ontouchcancel',
    'create_onload', 'create_onunload', 'create_onresize', 'create_onscroll',
    'create_ondrag', 'create_ondragstart', 'create_ondragend', 'create_ondragenter',
    'create_ondragleave', 'create_ondragover', 'create_ondrop',
    'create_onplay', 'create_onpause', 'create_onended', 'create_onvolumechange',
    'create_ontimeupdate', 'create_onseeking', 'create_onseeked',
    'create_onloadstart', 'create_onprogress', 'create_onerror', 'create_onabort',
    'create_onanimationstart', 'create_onanimationend', 'create_onanimationiteration',
    'create_ontransitionend', 'create_ontransitionrun', 'create_ontransitionstart',
    'create_onwheel', 'create_oncopy', 'create_oncut', 'create_onpaste',
    'create_onbeforeprint', 'create_onafterprint', 'create_onstorage',
    'create_onopen', 'create_onmessage', 'create_onclose', 'create_oninstall', 'create_onactivate',
    
    # PSX Utils
    'compile_psx', 'compile_psx_file', 'is_psx_file', 'PSXCompiler',
    
    # Legacy hooks
    'legacy_useState', 'legacy_useEffect', 'legacy_useContext', 'legacy_useReducer',
    'legacy_useCallback', 'legacy_useMemo', 'legacy_useRef', 'legacy_useCounter',
    'legacy_useToggle', 'legacy_useLocalStorage', 'legacy_useFetch', 'legacy_useDebounce',
]


maintainers = [
    {"name": "NextPy Team", "email": "team@nextpy.dev"}
]

main = "nextpy.server.app:create_app"