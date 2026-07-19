"""
NextPy PSX Hydration Module
Client-side interactivity for PSX components
"""

from .engine import HydrationEngine, HydrationContext, get_hydration_engine
from .integration import ComponentHydrator, get_component_hydrator, hydrate_component
from .decorators import interactive_component, enable_hydration_globally, create_interactive_page

__all__ = [
    # Core Engine
    'HydrationEngine',
    'HydrationContext',
    'get_hydration_engine',
    
    # Integration
    'ComponentHydrator',
    'get_component_hydrator',
    'hydrate_component',
    
    # Decorators
    'interactive_component',
    'enable_hydration_globally',
    'create_interactive_page',
]
