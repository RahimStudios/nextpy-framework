"""
React-like hooks for NextPy
Provides useState, useEffect, useReducer, useContext, useRef, useMemo, useCallback
and custom hooks like useCounter, useToggle, useLocalStorage, useFetch, useDebounce
"""

import threading
import time
import uuid
from typing import Any, Dict, List, Callable, Optional, TypeVar, Union
from dataclasses import dataclass, field

T = TypeVar('T')


@dataclass
class HookState:
    """State for a component using hooks"""
    component_id: str
    hooks: List[Dict[str, Any]] = field(default_factory=list)
    hook_index: int = 0
    state: Dict[str, Any] = field(default_factory=dict)
    cleanup_functions: List[Callable] = field(default_factory=list)


# Thread-local storage for hooks
_hook_state = threading.local()


def get_current_component() -> HookState:
    """Get current component's hook state"""
    if not hasattr(_hook_state, 'current'):
        _hook_state.current = {}
    
    thread_id = threading.get_ident()
    if thread_id not in _hook_state.current:
        _hook_state.current[thread_id] = HookState(component_id=str(uuid.uuid4()))
    
    return _hook_state.current[thread_id]


def reset_hooks():
    """Reset hooks for new render"""
    if hasattr(_hook_state, 'current'):
        thread_id = threading.get_ident()
        if thread_id in _hook_state.current:
            state = _hook_state.current[thread_id]
            state.hook_index = 0
            state.cleanup_functions.clear()


def cleanup_effects():
    """Run all cleanup functions"""
    if hasattr(_hook_state, 'current'):
        thread_id = threading.get_ident()
        if thread_id in _hook_state.current:
            state = _hook_state.current[thread_id]
            for cleanup in state.cleanup_functions:
                try:
                    cleanup()
                except:
                    pass
            state.cleanup_functions.clear()


# Core Hooks

def useState(initial_value: T) -> tuple[T, Callable[[T], None]]:
    """
    useState hook - just like React's useState
    Returns [value, setter] tuple
    
    Example:
        [count, setCount] = useState(0)
        setCount(count + 1)
    """
    component = get_current_component()
    
    if component.hook_index >= len(component.hooks):
        hook_data = {'value': initial_value, 'queue': []}
        component.hooks.append(hook_data)
    else:
        hook_data = component.hooks[component.hook_index]
    
    if hook_data['queue']:
        hook_data['value'] = hook_data['queue'][-1]
        hook_data['queue'] = []
    
    current_value = hook_data['value']
    
    def setter(new_value: T):
        if callable(new_value):
            new_value = new_value(current_value)
        hook_data['queue'].append(new_value)
        component.state['_needs_rerender'] = True
    
    component.hook_index += 1
    return current_value, setter


def useEffect(effect: Callable, deps: Optional[List[Any]] = None):
    """
    useEffect hook - just like React's useEffect
    Runs side effects and cleanup functions
    
    Example:
        useEffect(() => {
            console.log('Mounted')
            return () => console.log('Cleanup')
        }, [dependency])
    """
    component = get_current_component()
    
    if component.hook_index >= len(component.hooks):
        hook_data = {'deps': deps, 'cleanup': None, 'has_run': False}
        component.hooks.append(hook_data)
    else:
        hook_data = component.hooks[component.hook_index]
    
    # Check if dependencies changed
    deps_changed = False
    if deps is None:
        deps_changed = True
    elif hook_data['deps'] is None:
        deps_changed = True
    elif len(deps) != len(hook_data['deps']):
        deps_changed = True
    else:
        for i, dep in enumerate(deps):
            if dep != hook_data['deps'][i]:
                deps_changed = True
                break
    
    if deps_changed or not hook_data['has_run']:
        # Run cleanup if it exists
        if hook_data['cleanup']:
            try:
                hook_data['cleanup']()
            except:
                pass
        
        # Run effect
        try:
            cleanup = effect()
            if callable(cleanup):
                component.cleanup_functions.append(cleanup)
                hook_data['cleanup'] = cleanup
        except:
            pass
        
        hook_data['deps'] = deps
        hook_data['has_run'] = True
    
    component.hook_index += 1


def useReducer(reducer: Callable, initial_state: Any) -> tuple[Any, Callable]:
    """
    useReducer hook - just like React's useReducer
    Complex state management with reducer function
    
    Example:
        def counterReducer(state, action):
            if action['type'] == 'increment':
                return {'count': state['count'] + 1}
            return state
        
        [state, dispatch] = useReducer(counterReducer, {'count': 0})
        dispatch({'type': 'increment'})
    """
    component = get_current_component()
    
    if component.hook_index >= len(component.hooks):
        hook_data = {'state': initial_state}
        component.hooks.append(hook_data)
    else:
        hook_data = component.hooks[component.hook_index]
    
    current_state = hook_data['state']
    
    def dispatch(action: Any):
        new_state = reducer(current_state, action)
        hook_data['state'] = new_state
        component.state['_needs_rerender'] = True
    
    component.hook_index += 1
    return current_state, dispatch


def useContext(context: 'Context') -> Any:
    """
    useContext hook - just like React's useContext
    Access context values
    
    Example:
        ThemeContext = createContext('theme', 'light')
        theme = useContext(ThemeContext)
    """
    component = get_current_component()
    
    # For simplicity, just return the default value
    # In a real implementation, this would use a context provider
    return context.default_value


def useRef(initial_value: Any = None) -> Dict[str, Any]:
    """
    useRef hook - just like React's useRef
    Mutable ref object that persists across renders
    
    Example:
        inputRef = useRef()
        inputRef.current = 'value'
    """
    component = get_current_component()
    
    if component.hook_index >= len(component.hooks):
        hook_data = {'current': initial_value}
        component.hooks.append(hook_data)
    else:
        hook_data = component.hooks[component.hook_index]
    
    component.hook_index += 1
    return hook_data


def useMemo(factory: Callable, deps: Optional[List[Any]] = None) -> Any:
    """
    useMemo hook - just like React's useMemo
    Memoized value that only recalculates when dependencies change
    
    Example:
        expensiveValue = useMemo(() => calculateExpensiveValue(data), [data])
    """
    component = get_current_component()
    
    if component.hook_index >= len(component.hooks):
        hook_data = {'deps': deps, 'value': None, 'has_calculated': False}
        component.hooks.append(hook_data)
    else:
        hook_data = component.hooks[component.hook_index]
    
    # Check if dependencies changed
    deps_changed = False
    if deps is None:
        deps_changed = True
    elif hook_data['deps'] is None:
        deps_changed = True
    elif len(deps) != len(hook_data['deps']):
        deps_changed = True
    else:
        for i, dep in enumerate(deps):
            if dep != hook_data['deps'][i]:
                deps_changed = True
                break
    
    if deps_changed or not hook_data['has_calculated']:
        hook_data['value'] = factory()
        hook_data['deps'] = deps
        hook_data['has_calculated'] = True
    
    component.hook_index += 1
    return hook_data['value']


def useCallback(callback: Callable, deps: Optional[List[Any]] = None) -> Callable:
    """
    useCallback hook - just like React's useCallback
    Memoized callback that only changes when dependencies change
    
    Example:
        handleClick = useCallback(() => setCount(count + 1), [count])
    """
    return useMemo(lambda: callback, deps)


# Custom Hooks

def useCounter(initial_value: int = 0) -> tuple[int, Callable, Callable]:
    """
    Custom hook for counter functionality
    Returns [count, increment, decrement]
    
    Example:
        [count, increment, decrement] = useCounter(10)
        increment()
        decrement()
    """
    [count, setCount] = useState(initial_value)
    
    def increment():
        setCount(count + 1)
    
    def decrement():
        setCount(count - 1)
    
    return count, increment, decrement


def useToggle(initial_value: bool = False) -> tuple[bool, Callable]:
    """
    Custom hook for toggle functionality
    Returns [value, toggle]
    
    Example:
        [visible, toggle] = useToggle(True)
        toggle()
    """
    [value, setValue] = useState(initial_value)
    
    def toggle():
        setValue(not value)
    
    return value, toggle


def useLocalStorage(key: str, initial_value: Any) -> tuple[Any, Callable]:
    """
    Custom hook for localStorage persistence
    Returns [value, setValue]
    
    Example:
        [name, setName] = useLocalStorage('name', 'Guest')
        setName('John')
    """
    # For simplicity, just use useState
    # In a real implementation, this would use browser localStorage
    [value, setValue] = useState(initial_value)
    
    return value, setValue


def useFetch(url: str) -> Dict[str, Any]:
    """
    Custom hook for API data fetching
    Returns data object with data, loading, error, refetch
    
    Example:
        data = useFetch('/api/users')
        if data['loading']: return <div>Loading...</div>
        if data['error']: return <div>Error</div>
        return <div>{data['data']}</div>
    """
    [data, setData] = useState(None)
    [loading, setLoading] = useState(True)
    [error, setError] = useState(None)
    
    def refetch():
        setLoading(True)
        setError(None)
        # In a real implementation, this would make an HTTP request
        try:
            # Simulate API call
            time.sleep(0.1)
            setData({'message': f'Data from {url}'})
        except Exception as e:
            setError(str(e))
        finally:
            setLoading(False)
    
    useEffect(refetch, [url])
    
    return {
        'data': data,
        'loading': loading,
        'error': error,
        'refetch': refetch
    }


def useDebounce(value: Any, delay: int) -> Any:
    """
    Custom hook for debouncing values
    Returns debounced value
    
    Example:
        debouncedSearch = useDebounce(searchTerm, 500)
    """
    [debouncedValue, setDebouncedValue] = useState(value)
    
    def setup_debounce():
        def timeout_callback():
            setDebouncedValue(value)
        
        handler = setTimeout(timeout_callback, delay)
        
        return lambda: clearTimeout(handler)
    
    useEffect(setup_debounce, [value, delay])
    
    return debouncedValue


# Context API

@dataclass
class Context:
    """Context object for useContext hook"""
    name: str
    default_value: Any


def createContext(name: str, default_value: Any) -> Context:
    """
    Create a context object
    Returns context that can be used with useContext and Provider
    
    Example:
        ThemeContext = createContext('theme', 'light')
    """
    return Context(name=name, default_value=default_value)


class Provider:
    """Provider for context values"""
    
    def __init__(self, context: Context, value: Any, children=None):
        self.context = context
        self.value = value
        self.children = children


# Timer functions (simplified)
def setTimeout(callback: Callable, delay: int) -> str:
    """Simulated setTimeout"""
    timer_id = str(uuid.uuid4())
    
    def timer_thread():
        time.sleep(delay / 1000.0)
        try:
            callback()
        except:
            pass
    
    thread = threading.Thread(target=timer_thread)
    thread.daemon = True
    thread.start()
    
    return timer_id


def clearTimeout(timer_id: str):
    """Simulated clearTimeout"""
    # In a real implementation, this would cancel the timer
    pass


def setInterval(callback: Callable, interval: int) -> str:
    """Simulated setInterval"""
    timer_id = str(uuid.uuid4())
    
    def interval_thread():
        while True:
            time.sleep(interval / 1000.0)
            try:
                callback()
            except:
                break
    
    thread = threading.Thread(target=interval_thread)
    thread.daemon = True
    thread.start()
    
    return timer_id


def clearInterval(timer_id: str):
    """Simulated clearInterval"""
    # In a real implementation, this would cancel the interval
    pass