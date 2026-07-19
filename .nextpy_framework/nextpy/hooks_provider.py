"""
Hooks Provider - Integrates hooks with the component system
Enables React-like hooks in NextPy components
"""

from typing import Any, Dict, List, Callable, Optional
from .hooks import (
    useState, useEffect, useReducer, useContext, useRef, 
    useMemo, useCallback, reset_hooks, cleanup_effects,
    useCounter, useToggle, useLocalStorage, useFetch, useDebounce,
    createContext, Provider as ContextProvider
)
from .jsx import JSXElement, render_jsx


class HooksProvider:
    """Provider for React-like hooks in components"""
    
    def __init__(self):
        self.components = {}
        self.render_queue = []
    
    def render_component_with_hooks(self, component_func: Callable, props: Dict = None) -> JSXElement:
        """
        Render a component function with hooks support
        Similar to React's component rendering
        """
        if props is None:
            props = {}
        
        # Reset hooks for new render
        reset_hooks()
        
        try:
            # Call the component function
            result = component_func(props)
            
            # Check if component needs re-render due to state changes
            from .hooks import get_current_component
            component_state = get_current_component()
            
            if component_state.state.get('_needs_rerender'):
                # Re-render the component
                component_state.state['_needs_rerender'] = False
                reset_hooks()
                result = component_func(props)
            
            return result
            
        except Exception as e:
            # Return error element
            from .jsx import div, h2, p
            return div({'className': 'error'},
                h2({}, 'Component Error'),
                p({}, str(e))
            )
    
    def create_hooked_component(self, component_func: Callable) -> Callable:
        """
        Create a component that supports hooks
        This is the main function to wrap components with hook support
        """
        def hooked_component(props: Dict = None):
            if props is None:
                props = {}
            
            return self.render_component_with_hooks(component_func, props)
        
        return hooked_component
    
    def cleanup(self):
        """Cleanup all hooks and effects"""
        cleanup_effects()


# Global hooks provider instance
hooks_provider = HooksProvider()


def with_hooks(component_func: Callable) -> Callable:
    """
    Decorator to add hook support to a component
    Usage:
        @with_hooks
        def MyComponent(props):
            [count, setCount] = useState(0)
            return div({}, f'Count: {count}')
    """
    return hooks_provider.create_hooked_component(component_func)


# Component wrapper for hooks
def HookComponent(render_func: Callable):
    """
    Create a component with hook support
    Usage:
        MyComponent = HookComponent(lambda props: {
            [count, setCount] = useState(0)
            return div({}, f'Count: {count}')
        })
    """
    return with_hooks(render_func)


# Export the main functions
__all__ = [
    'HooksProvider', 'with_hooks', 'HookComponent', 'hooks_provider',
    # Re-export all hooks
    'useState', 'useEffect', 'useReducer', 'useContext', 'useRef',
    'useMemo', 'useCallback',
    'useCounter', 'useToggle', 'useLocalStorage', 'useFetch', 'useDebounce',
    'createContext', 'ContextProvider'
]
