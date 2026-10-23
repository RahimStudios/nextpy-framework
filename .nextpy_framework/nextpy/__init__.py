"""
NextPy - The Python Web Framework
Full-stack framework with file-based routing, SSR, SSG, and enhanced client-server sync
"""

__version__ = "5.0.0"

from nextpy.core.router import Router, Route, DynamicRoute
from nextpy.core.renderer import Renderer
from nextpy.core.data_fetching import (
    get_server_side_props,
    get_static_props,
    get_static_paths,
)
from nextpy.components.head import Head
from nextpy.components.link import Link
from nextpy.server.app import create_app, get_api_app
from nextpy.db import (
    Base, Model, Database, get_db, get_session, session, init_db,
    Page, paginate, transaction, get_or_none, get_or_404, batch_get,
    apply_filters, eager_load, serialize_model, count_by,
)
from nextpy.cache import MemoryCache, cached, get_cache, invalidate
from nextpy.tasks import BackgroundQueue, get_queue, enqueue, task as background_task
from nextpy.api import api, fetch_api
from nextpy.admin import AdminSite, admin, register
from nextpy.auth import (
    AuthManager, require_auth, create_session,
    get_session as get_auth_session, delete_session,
    hash_password, verify_password,
    set_session_cookie, get_user_id_from_request, clear_session_cookie,
    get_user_from_request, current_user_id, require_user, require_role,
)

# Enhanced full-stack features
from nextpy.server_actions import (
    ServerAction, server_action, ServerActionError, ValidationError,
    FormValidator, ActionSchema, get_health_status, get_current_user
)
from nextpy.state_sync import (
    StateManager, get_state_manager, get_state, set_state, update_state, delete_state,
    ServerState, DatabaseState
)

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
    useCounter, useToggle, useLocalStorage, useFetch, useAction, useDebounce,
    useInterval, usePrevious, useAsync, useMediaQuery, useGeolocation, usePerformance,
    
    # Server action bridge
    callServerAction,
    
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
    'Router', 'Route', 'DynamicRoute', 'Renderer', 'create_app', 'get_api_app',
    'Base', 'Model', 'Database', 'init_db', 'get_db', 'get_session', 'session', 'api', 'fetch_api',
    'Page', 'paginate', 'transaction', 'get_or_none', 'get_or_404', 'batch_get',
    'apply_filters', 'eager_load', 'serialize_model', 'count_by',
    'MemoryCache', 'cached', 'get_cache', 'invalidate',
    'BackgroundQueue', 'get_queue', 'enqueue', 'background_task',
    'AuthManager', 'require_auth', 'create_session', 'get_auth_session', 'delete_session',
    'hash_password', 'verify_password', 'set_session_cookie', 'get_user_id_from_request', 'clear_session_cookie',
    'get_user_from_request', 'current_user_id', 'require_user', 'require_role',
    'get_server_side_props', 'get_static_props', 'get_static_paths',
    'Head', 'Link', 'AdminSite', 'admin', 'register',
    
    # Enhanced Full-Stack Features
    'ServerAction', 'server_action', 'ServerActionError', 'ValidationError',
    'FormValidator', 'ActionSchema', 'get_health_status', 'get_current_user',
    'StateManager', 'get_state_manager', 'get_state', 'set_state', 'update_state', 'delete_state',
    'ServerState', 'DatabaseState',
    
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
    'useCounter', 'useToggle', 'useLocalStorage', 'useFetch', 'useAction', 'useDebounce',
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