"""
Component Hydrator - Clean integration with hydration engine
Works with the new engine architecture for proper component management
"""

import sys
import inspect
import ast
import re
from typing import Dict, Any, Optional, Callable, List
from .engine import get_hydration_engine, HydrationEngine


class ComponentHydrator:
    """
    Clean component hydrator that works with the new engine
    """
    
    def __init__(self, engine: Optional[HydrationEngine] = None):
        self.engine = engine or get_hydration_engine()
    
    def extract_component_metadata(self, component_func: Callable) -> Dict[str, Any]:
        """Extract component metadata from function"""
        return {
            "name": component_func.__name__,
            "state": self._extract_state(component_func),
            "handlers": self._extract_handlers(component_func),
            "effects": self._extract_effects(component_func),
        }
    
    def _extract_state(self, component_func: Callable) -> Dict[str, Any]:
        """Extract state from useState calls using regex"""
        try:
            # Try to get the original file path
            file_path = None
            if hasattr(component_func, '__module__') and component_func.__module__ in sys.modules:
                module = sys.modules[component_func.__module__]
                if hasattr(module, '__original_file__'):
                    file_path = module.__original_file__
            
            if file_path:
                # Read the original file
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
            else:
                # Fallback to inspect.getsource
                source = inspect.getsource(component_func)
            
            # Use regex to find useState patterns
            pattern = r'\[(\w+),\s*set\w+\]\s*=\s*useState\s*\(\s*([^)]*)\s*\)'
            matches = re.findall(pattern, source)
            
            state = {}
            for var_name, initial_value in matches:
                try:
                    # Safely evaluate the initial value
                    if initial_value.strip().startswith(('"') or initial_value.strip().startswith("'")):
                        value = initial_value.strip()[1:-1]
                    else:
                        value = ast.literal_eval(initial_value.strip())
                    state[var_name] = value
                except:
                    state[var_name] = initial_value.strip()
            
            return state
        except Exception as e:
            print(f"Warning: Could not extract state: {e}")
            return {}
    
    def _extract_handlers(self, component_func: Callable) -> Dict[str, str]:
        """Extract handlers from _handlers attribute or function definition"""
        # Check if handlers are defined as attribute (new way)
        if hasattr(component_func, '_handlers'):
            return getattr(component_func, '_handlers', {})
        
        # Fallback to extracting from function source
        try:
            source = inspect.getsource(component_func)
            lines = source.split('\n')
            handlers = {}
            
            for line in lines:
                # Match handler functions at component level (4+ spaces)
                match = re.match(r'^    def\s+((?:handle|on)_\w+)\s*\([^)]*\)\s*:', line)
                if match:
                    handler_name = match.group(1)
                    # Extract function body
                    func_lines = []
                    i = lines.index(line) + 1
                    while i < len(lines):
                        next_line = lines[i]
                        # Stop if we hit another def or end of component
                        if next_line.startswith('    def ') or (next_line and not next_line.startswith('        ')):
                            break
                        # Add if it's body (starts with 8 spaces)
                        if next_line.startswith('        '):
                            func_lines.append(next_line[8:])  # Remove 8 spaces
                        i += 1
                    
                    # Store handler
                    body = '\n'.join(func_lines).strip()
                    if body:
                        handlers[handler_name] = body
            return handlers
        except Exception as e:
            return {}  # Changed from return(str(e)) to return {}
    
    def _extract_effects(self, component_func: Callable) -> List[Dict[str, Any]]:
        """Extract useEffect calls from component"""
        try:
            # Try to get the original file path
            file_path = None
            if hasattr(component_func, '__module__') and component_func.__module__ in sys.modules:
                module = sys.modules[component_func.__module__]
                if hasattr(module, '__original_file__'):
                    file_path = module.__original_file__
            
            if file_path:
                # Read the original file
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
            else:
                # Fallback to inspect.getsource
                source = inspect.getsource(component_func)
            
            # Use the existing _extract_effects_from_source method
            return self._extract_effects_from_source(source)
        except Exception as e:
            print(f"Warning: Could not extract effects: {e}")
            return []
    
    def _extract_effects_from_source(self, source: str) -> List[Dict[str, Any]]:
        """Extract useEffect calls from source"""
        effects = []
        
        # Match useEffect patterns
        pattern = r'useEffect\s*\(\s*([^,]+)\s*,\s*(\[[^\]]*\])\s*\)'
        matches = re.findall(pattern, source)
        
        for func_name, deps in matches:
            effects.append({
                'function': func_name.strip(),
                'dependencies': deps,
            })
        
        return effects
    
    def register_component(self, component_func: Callable, props: Dict[str, Any] = None) -> str:
        """Register a component for hydration"""
        metadata = self.extract_component_metadata(component_func)
        
        # Execute the component function to get the result
        if props is None:
            result = component_func()
        else:
            result = component_func(props)
        
        # Handle different return types
        if hasattr(result, 'to_html'):
            # This is a PSX element - get the HTML
            html = result.to_html()
        elif hasattr(result, '__html__'):
            # This is an HTML string
            html = result.__html__
        else:
            # Convert to HTML string
            html = str(result)
        
        # Use the engine's HTML wrapper to properly hydrate the component
        component_id = self.engine.register_component({
            'name': metadata['name'],
            'state': metadata['state'],
            'handlers': metadata['handlers'],
            'effects': metadata.get('effects', []),
            'props': props or {},
        })
        wrapped_html = self.engine.generate_html_wrapper(component_id, html, metadata['state'])
        
        # Generate hydration script for all components
        hydration_script = self.engine.generate_hydration_script()
        
        # Combine HTML and script
        return f"{wrapped_html}\n<script type='text/javascript'>\n{hydration_script}\n</script>"
    
    def wrap_component_html(self, component_id: str, html: str, 
                          state: Dict[str, Any]) -> str:
        """Wrap component HTML with hydration data"""
        return self.engine.generate_html_wrapper(component_id, html, state)
    
    def generate_hydration_script(self) -> str:
        """Generate complete hydration script"""
        return self.engine.generate_hydration_script()


# Global component hydrator instance
_component_hydrator = ComponentHydrator()


def get_component_hydrator() -> ComponentHydrator:
    """Get the global component hydrator"""
    return _component_hydrator


def hydrate_component(component_func: Callable, props: Dict[str, Any], 
                     html: str) -> tuple[str, str]:
    """
    Hydrate a component with interactivity
    
    Returns: (hydrated_html, hydration_script)
    """
    hydrator = get_component_hydrator()
    component_id = hydrator.register_component(component_func, props)
    
    # Extract state from metadata
    metadata = hydrator.extract_component_metadata(component_func)
    state = metadata['state']
    
    # Wrap HTML with hydration data
    hydrated_html = hydrator.wrap_component_html(component_id, html, state)
    
    # Generate hydration script
    hydration_script = hydrator.generate_hydration_script()
    
    return hydrated_html, hydration_script
