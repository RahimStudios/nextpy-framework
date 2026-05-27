"""
PRODUCTION FIX: Handler Registration System
Properly converts Python event handlers to JavaScript and registers them.
"""

# Fix: Instead of referencing Python functions directly, we extract and register them

# The problem:
# ❌ <button onClick={handle_increment}>  <- Python function, doesn't exist in JS
# 
# The solution:
# ✅ <button data-handler="handle_increment">  <- Reference by ID
# ✅ NextPyRuntime.registerHandler('handle_increment', (e) => { ... })

import re
import inspect
from typing import Dict, List, Callable, Any

class HandlerExtractor:
    """Extracts Python event handlers and converts them to JavaScript"""
    
    def __init__(self):
        self.handlers: Dict[str, str] = {}
    
    def extract_handlers(self, component_func: Callable) -> Dict[str, str]:
        """Extract all named handler functions from component source"""
        handlers = {}
        
        try:
            source = inspect.getsource(component_func)
        except (OSError, TypeError):
            return handlers
        
        # Find all function definitions that look like handlers
        # Pattern: def handle_* or def on_*
        pattern = r'def\s+(handle_\w+|on_\w+)\s*\(\s*e?\s*\)\s*:\s*\n((?:\s{4}[^\n]*(?:\n|$))*)'
        
        matches = re.finditer(pattern, source)
        for match in matches:
            func_name = match.group(1)
            func_body = match.group(2)
            
            # Clean up indentation
            lines = func_body.split('\n')
            cleaned_lines = [line[4:] if line.startswith('    ') else line for line in lines]
            cleaned_body = '\n'.join(cleaned_lines).strip()
            
            handlers[func_name] = cleaned_body
        
        return handlers
    
    def python_to_js(self, handler_name: str, handler_body: str) -> str:
        """Convert Python handler code to JavaScript"""
        js_code = handler_body
        
        # Replace Python function calls with JS equivalents
        replacements = {
            # setState pattern: setCount(count + 1) -> this.setState('count', count + 1)
            r'set(\w+)\(([^)]+)\)': r"this.setState('\1', \2)",
            # Comparison operators (already same in JS, but be explicit)
            r'==': '===',
            r'!=': '!==',
            # Print to console
            r'print\(': 'console.log(',
        }
        
        for pattern, replacement in replacements.items():
            js_code = re.sub(pattern, replacement, js_code)
        
        return js_code
    
    def generate_handler_script(self, handlers: Dict[str, str]) -> str:
        """Generate JavaScript to register all handlers"""
        if not handlers:
            return ""
        
        script = """
// Register event handlers
(function() {
    const componentId = NextPyRuntime.currentComponentId;
    const component = NextPyRuntime.components.get(componentId);
    
    if (!component) return;
    
"""
        
        for handler_name, handler_body in handlers.items():
            js_body = self.python_to_js(handler_name, handler_body)
            
            script += f"""
    // {handler_name}
    component.registerHandler('{handler_name}', function(e) {{
        {js_body}
    }});
"""
        
        script += """
})();
"""
        return script


# Example usage in hydration integration:

def extract_handlers_from_component(component_func: Callable) -> Dict[str, str]:
    """Extract all handlers from a component"""
    extractor = HandlerExtractor()
    return extractor.extract_handlers(component_func)


def convert_handler_references(html: str, handlers: Dict[str, str]) -> str:
    """Convert onClick={handle_name} to data-handler="handle_name" """
    
    # Pattern: onClick={handle_name} or onclick={handler_name}
    pattern = r'(?:onClick|onclick)=\{(\w+)\}'
    
    def replace_handler(match):
        handler_name = match.group(1)
        if handler_name in handlers:
            # Use data attribute instead
            return f'data-handler="{handler_name}"'
        return match.group(0)
    
    return re.sub(pattern, replace_handler, html)


# USAGE in decorators.py:
# 
# from .handler_system import extract_handlers_from_component, convert_handler_references
# 
# def interactive_component(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         # Extract handlers from component
#         handlers = extract_handlers_from_component(func)
#         
#         # ... render component ...
#         html = base_component(func)(*args, **kwargs)
#         
#         # Convert handler references in HTML
#         html = convert_handler_references(html, handlers)
#         
#         # Generate handler registration script
#         handler_script = HandlerExtractor().generate_handler_script(handlers)
#         
#         # Include in full script
#         complete_script = f"{full_script}\n\n{handler_script}"
#         
#         return InteractiveComponentResult(html, complete_script)
