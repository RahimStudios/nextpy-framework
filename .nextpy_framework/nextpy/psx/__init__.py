"""
PSX Package - Clean Python Syntax eXtension for NextPy
Production-ready PSX with clean architecture
"""

# Core imports
from .core.parser import PSXElement, PSXParser, psx, render_psx, fragment, key
from .core.runtime import process_python_logic, runtime
from .core.evaluator import SafeExpressionEngine
from .vdom.vnode import VNode, create_element, render, update, get_vdom_metrics
from .renderer.renderer import PSXRenderer, renderer
from .components.component import (
    PSXComponent, component, class_component, ChildrenComponent,
    register_component, clsx,
    # React Hooks
    useState, useEffect, useContext, useReducer, useRef, useMemo, useCallback,
    useImperativeHandle, useLayoutEffect, useDebugValue, useTransition,
    useDeferredValue, useId,
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
    create_onopen, create_onmessage, create_onclose, create_oninstall, create_onactivate
)
from .utils.helpers import compile_psx, compile_psx_file, is_psx_file, PSXCompiler

# Hydration Engine imports
from .hydration import (
    HydrationEngine, get_hydration_engine,
    interactive_component, enable_hydration_globally, create_interactive_page,
    hydrate_component, get_component_hydrator,
)

# Convenience functions
def render_psx_component(element, context=None):
    """Render PSX component using the clean renderer"""
    html = renderer.render(element, context)
    
    # Inject JavaScript runtime script for interactive components and full HTML documents
    try:
        from .runtime.js_actions_runtime import JS_ACTION_RUNTIME_SCRIPT
        # Always inject for interactive components or full HTML documents
        if 'data-handler-' in html or 'data-bind' in html or '<html' in html:
            # Insert script at the very beginning to ensure it loads first
            html = f"<script>{JS_ACTION_RUNTIME_SCRIPT}</script>{html}"
    except ImportError:
        pass
    
    return html

# Auto-export all PSX features
__all__ = [
    # Core
    'PSXElement', 'PSXParser', 'psx', 'render_psx', 'fragment', 'key',
    'process_python_logic', 'runtime', 'SafeExpressionEngine',
    
    # VDOM
    'VNode', 'create_element', 'render', 'update', 'get_vdom_metrics',
    
    # Renderer
    'PSXRenderer', 'renderer', 'render_psx_component',
    
    # Components
    'PSXComponent', 'component', 'class_component', 'ChildrenComponent',
    'register_component', 'clsx',
    
    # React Hooks
    'useState', 'useEffect', 'useContext', 'useReducer', 'useRef',
    'useMemo', 'useCallback', 'useImperativeHandle', 'useLayoutEffect',
    'useDebugValue', 'useTransition', 'useDeferredValue', 'useId',
    
    # Custom Hooks
    'useCounter', 'useToggle', 'useLocalStorage', 'useFetch', 'useDebounce',
    'useInterval', 'usePrevious', 'useAsync', 'useMediaQuery', 'useGeolocation', 'usePerformance',
    
    # Event Handlers
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
    
    # Utils
    'compile_psx', 'compile_psx_file', 'is_psx_file', 'PSXCompiler',
    
    # Hydration Engine
    'HydrationEngine', 'get_hydration_engine',
    'interactive_component', 'enable_hydration_globally', 'create_interactive_page',
    'hydrate_component', 'get_component_hydrator',
]
