"""
Interactive Component Decorator for NextPy PSX - PRODUCTION VERSION
Enables client-side interactivity with proper handler registration
"""

import sys
import inspect
import re
import ast
import hashlib
import html as html_module
import json
from functools import wraps
from typing import Callable, Dict, Any, Optional, List


def extract_handler_functions(component_func: Callable) -> Dict[str, str]:
    """
    Extract all named event handler functions from component source.
    
    Returns: {handler_name: handler_code}
    """
    handlers = {}
    
    try:
        # Try to get source - might be wrapped
        source = inspect.getsource(component_func)
    except (OSError, TypeError):
        return handlers
    
    # Only parse the component body before the return statement
    lines = source.split('\n')
    component_lines = []
    in_def = False
    for line in lines:
        if re.match(r'^\s*def\b', line):
            in_def = True
        if in_def:
            if re.match(r'^\s*return\b', line):
                break
            component_lines.append(line)
    
    source = '\n'.join(component_lines)
    
    # Split by function definitions at component or nested function level
    lines = source.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        # Look for nested def handle_* or def on_* definitions
        match = re.match(r'^(\s+)def\s+((?:handle|on)_\w+)\s*\([^)]*\)\s*:', line)
        if match:
            indent = len(match.group(1))
            func_name = match.group(2)
            func_lines = []
            i += 1
            # Collect lines until next def at same or lesser indentation
            while i < len(lines):
                next_line = lines[i]
                if not next_line.strip():
                    func_lines.append('')
                    i += 1
                    continue
                next_indent = len(next_line) - len(next_line.lstrip(' '))
                if next_indent <= indent:
                    break
                # Remove the extra indentation for the function body
                if next_indent >= indent + 4:
                    func_lines.append(next_line[indent + 4:])
                else:
                    func_lines.append(next_line.lstrip(' '))
                i += 1
            
            body = '\n'.join(func_lines).rstrip()
            if body:
                handlers[func_name] = body
        else:
            i += 1
    
    return handlers


def _get_python_call_placeholder_from_ast(arg: ast.expr) -> str:
    if isinstance(arg, ast.Name):
        return f"python_call_{arg.id}"

    if isinstance(arg, ast.Lambda):
        try:
            lambda_src = ast.unparse(arg).strip()
            normalized = re.sub(r'\s+', ' ', lambda_src)
            digest = hashlib.sha256(normalized.encode('utf-8')).hexdigest()[:16]
            return f"python_call_lambda_{digest}"
        except Exception:
            return f"python_call_lambda_{hash(ast.dump(arg))}"

    return "python_call_handler"


def extract_create_handler_assignments(component_func: Callable, existing_handlers: Optional[Dict[str, str]] = None) -> (Dict[str, str], Dict[str, str]):
    """
    Extract handlers created with create_on... utility functions.
    Returns a tuple of (handlers, event_types).
    """
    handlers: Dict[str, str] = {}
    event_types: Dict[str, str] = {}

    try:
        source = inspect.getsource(component_func)
    except (OSError, TypeError):
        return handlers, event_types

    # Only parse the component body before the return statement
    lines = source.split('\n')
    body_lines = []
    in_def = False
    for line in lines:
        if re.match(r'^\s*def\b', line):
            in_def = True
        if in_def:
            if re.match(r'^\s*return\b', line):
                break
            body_lines.append(line)

    try:
        tree = ast.parse('\n'.join(body_lines))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
                    continue

                target_name = node.targets[0].id
                value = node.value

                if isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
                    func_name = value.func.id
                    if func_name.startswith('create_on') and value.args:
                        event_name = func_name[len('create_on'):].lower()
                        arg = value.args[0]

                        if isinstance(arg, ast.Lambda):
                            try:
                                handler_body = ast.unparse(arg.body).strip()
                                placeholder = _get_python_call_placeholder_from_ast(arg)
                                if handler_body:
                                    handlers[target_name] = handler_body
                                    handlers[placeholder] = handler_body
                                    event_types[target_name] = event_name
                                    event_types[placeholder] = event_name
                            except Exception:
                                continue
                        elif isinstance(arg, ast.Name):
                            # The handler function is defined elsewhere
                            placeholder = _get_python_call_placeholder_from_ast(arg)
                            event_types[target_name] = event_name
                            event_types[placeholder] = event_name
                            if existing_handlers and arg.id in existing_handlers:
                                handlers[placeholder] = existing_handlers[arg.id]
    except Exception:
        pass

    return handlers, event_types


def replace_state_variables(expr: str, state_keys: Optional[List[str]] = None) -> str:
    """
    Replace state variables with stateManager.get calls in complex expressions
    """
    import re
    
    # Use provided state keys or fall back to common ones
    keys_to_check = state_keys if state_keys else ['count', 'name', 'loading', 'data', 'items', 'index', 'value', 'user', 'error', 'success']
    
    for potential_key in keys_to_check:
        # More sophisticated patterns to avoid false positives
        # Don't replace if part of a larger variable name, in quotes, or function call
        # Use negative lookbehind/lookahead to avoid quotes
        patterns = [
            # Standalone variable: count -> this.stateManager.get('count')
            # Not preceded by quote, not followed by quote or dot or bracket
            (rf'(?<![\'"])\b{potential_key}\b(?!\s*[\.\(\[])(?![\'"])', f'this.stateManager.get(\'{potential_key}\')'),
            # Method calls: name.upper() -> this.stateManager.get('name').upper()
            (rf'(?<![\'"])\b{potential_key}\b(?=\s*\.)(?![\'"])', f'this.stateManager.get(\'{potential_key}\')'),
            # Array access: items[0] -> this.stateManager.get('items')[0]
            (rf'(?<![\'"])\b{potential_key}\b(?=\s*\[)(?![\'"])', f'this.stateManager.get(\'{potential_key}\')'),
        ]
        
        for pattern, replacement in patterns:
            expr = re.sub(pattern, replacement, expr)
    return expr


def python_code_to_js(python_code: str, state_keys: Optional[List[str]] = None) -> str:
    """
    Convert Python event handler code to JavaScript.
    
    IMPROVED: More robust pattern matching and error handling.
    NOTE: This is a transitional approach. Future versions should use
    an instruction-based system instead of code translation.
    
    PATTERN SUPPORT:
    - setState(value) -> stateManager.set('state', value)
    - setXxxx(value) -> stateManager.set('xxx', value) [auto-camelCase conversion]
    - Function calls, operators, string literals
    - Python to JS equivalents (print -> console.log, and -> &&, etc.)
    
    LIMITATIONS:
    - Complex Python expressions may fail
    - Nested function calls have limited support
    - User input in state values could cause issues
    """
    js_code = python_code
    
    # Convert lambda to arrow function
    js_code = re.sub(r'lambda\s+(\w+):(.*)', r'(\1) => \2', js_code)
    
    # SECURITY: Prevent dangerous patterns
    dangerous_patterns = [
        r'eval\s*\(',
        r'__import__\s*\(',
        r'exec\s*\(',
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, js_code, re.IGNORECASE):
            print(f"⚠️ WARNING: Handler contains dangerous pattern: {pattern}")
            js_code = re.sub(pattern, '/* BLOCKED */ ', js_code)
    
    # Pattern 1: Replace setXxxx(expression) with stateManager.set patterns
    def replace_setter(match):
        setter_name = match.group(1)  # "Count" from "setCount"
        expression = match.group(2)   # The argument (may contain nested parens)
        state_key = setter_name[0].lower() + setter_name[1:]  # "count"
        
        # IMPROVED: Handle nested function calls better
        expression = expression.strip()
        
        # Replace state variables with stateManager.get calls
        # Handle patterns like: count + 1 -> this.stateManager.get('count') + 1
        
        # Handle enhanced nested patterns
        expr_js = expression
        expr_js = replace_state_variables(expr_js, state_keys)
        
        # Enhanced string method conversions
        string_conversions = [
            (r'\.upper\s*\(\s*\)', '.toUpperCase()'),
            (r'\.lower\s*\(\s*\)', '.toLowerCase()'),
            (r'\.strip\s*\(\s*\)', '.trim()'),
            (r'\.title\s*\(\s*\)', '.charAt(0).toUpperCase() + this.slice(1).toLowerCase()'),
            (r'\.replace\s*\(([^,]+),\s*([^)]+)\)', r'.replace($1, $2)'),
            (r'\.split\s*\(', '.split('),
            (r'\.join\s*\(', '.join('),
            (r'\.startswith\s*\(', '.startsWith('),
            (r'\.endswith\s*\(', '.endsWith('),
        ]
        
        # Enhanced list/array method conversions
        list_conversions = [
            (r'\.append\s*\(', '.push('),
            (r'\.extend\s*\(', '.concat('),
            (r'\.pop\s*\(', '.pop('),
            (r'\.remove\s*\(', '.filter(item => item !== '),  # Simplified
            (r'\.sort\s*\(', '.sort('),
            (r'\.reverse\s*\(', '.reverse('),
            (r'\.clear\s*\(', '.length = 0'),  # Simplified
        ]
        
        # Enhanced built-in function conversions
        builtin_conversions = [
            (r'\blen\s*\(\s*(\w+)\s*\)', r'$1.length'),
            (r'\bstr\s*\(', 'String('),
            (r'\bint\s*\(', 'parseInt('),
            (r'\bfloat\s*\(', 'parseFloat('),
            (r'\bbool\s*\(', 'Boolean('),
            (r'\btype\s*\(', 'typeof '),
            (r'\babs\s*\(', 'Math.abs('),
            (r'\bround\s*\(', 'Math.round('),
            (r'\bmin\s*\(', 'Math.min('),
            (r'\bmax\s*\(', 'Math.max('),
            (r'\bsum\s*\(', '.reduce((a, b) => a + b, 0)'),
        ]
        
        # Apply all conversions
        all_conversions = string_conversions + list_conversions + builtin_conversions
        for pattern, replacement in all_conversions:
            expr_js = re.sub(pattern, replacement, expr_js)
        
        return f"this.stateManager.set('{state_key}', {expr_js})"
    
    # Find all setXxxx(...) calls - IMPROVED regex to handle nested parens
    # This pattern matches setName(arg) where arg can contain balanced parens
    js_code = re.sub(
        r'set([A-Z]\w*)\s*\(([^)]*(?:\([^)]*\)[^)]*)*)\)',
        replace_setter,
        js_code
    )
    
    # Pattern 2: Additional global conversions
    global_replacements = [
        (r'\bprint\s*\(', 'console.log('),          # print() -> console.log()
        (r'\bTrue\b', 'true'),                      # True -> true
        (r'\bFalse\b', 'false'),                    # False -> false
        (r'\bNone\b', 'null'),                       # None -> null
    ]
    
    for pattern, replacement in global_replacements:
        js_code = re.sub(pattern, replacement, js_code)
    
    # Pattern 3: Enhanced logical operators (more precise patterns)
    logical_replacements = [
        (r'(?<!\w)\s*and\s*(?!\w)', ' && '),        # and -> &&
        (r'(?<!\w)\s*or\s*(?!\w)', ' || '),         # or -> ||
        (r'(?<!\w)\s*not\s*(?!\w)', '!'),            # not -> !
        (r'\s+is\s+None\s*', ' === null '),          # is None -> === null
        (r'\s+is\s+not\s+None\s*', ' !== null '),    # is not None -> !== null
        (r'\s+in\s+', ' in '),                       # in operator (preserved)
    ]
    
    for pattern, replacement in logical_replacements:
        js_code = re.sub(pattern, replacement, js_code)
    
    # Pattern 4: Handle any remaining state variables that weren't in setters
    js_code = replace_state_variables(js_code, state_keys)
    
    # Pattern 5: Final cleanup and normalization
    js_code = re.sub(r'\s+', ' ', js_code)  # Normalize whitespace
    js_code = js_code.strip()
    
    return js_code


def generate_handler_registration_script(
    handlers: Dict[str, str], 
    component_id: str,
    event_types: Optional[Dict[str, str]] = None,
    state_keys: Optional[List[str]] = None
) -> str:
    """
    Generate JavaScript to register all handlers for a component.
    
    IMPROVED: Supports multiple event types and dynamic binding.
    
    Args:
        handlers: {handler_name: handler_code}
        component_id: Component ID for scoping
        event_types: Optional {handler_name: 'click'|'change'|'submit'...}
        state_keys: Optional list of state variable names for better conversion
    """
    if not handlers:
        return ""
    
    # Default event type is 'click'
    if event_types is None:
        event_types = {name: 'click' for name in handlers}
    
    script = f"""
// Handler registration for component: {component_id}
(function() {{
    // Safety check: Ensure NextPyActionRuntime exists
    if (typeof window.NextPyActionRuntime === 'undefined') {{
        console.error('NextPyActionRuntime not found. Skipping handler registration for component: {component_id}');
        return;
    }}
    
    const componentId = '{component_id}';
    const component = window.nextpyComponents?.[componentId];
    
    if (!component) {{
        console.warn('Component not found: ' + componentId);
        return;
    }}
    
    // Store handlers on the component
    component._handlers = {{}};
"""
    
    for handler_name, handler_body in handlers.items():
        # Check if handler_body is already structured actions (list of Action objects or dicts)
        if isinstance(handler_body, list) and handler_body:
            if hasattr(handler_body[0], 'to_dict'):
                # New AST-based structured Action objects
                serialized_actions = [action.to_dict() for action in handler_body]
                js_body = f"executeNextPyActions({json.dumps(serialized_actions)}, componentId)"
                event_type = event_types.get(handler_name, 'click')
            elif isinstance(handler_body[0], dict):
                # Already serialized actions
                js_body = f"executeNextPyActions({json.dumps(handler_body)}, componentId)"
                event_type = event_types.get(handler_name, 'click')
            else:
                # Fallback to old python_code_to_js for string-based handlers
                js_body = python_code_to_js(handler_body, state_keys)
                event_type = event_types.get(handler_name, 'click')
        else:
            # Fallback to old python_code_to_js for string-based handlers
            js_body = python_code_to_js(handler_body, state_keys)
            event_type = event_types.get(handler_name, 'click')
        
        # Create the handler function with error handling
        script += f"""
    // Handler: {handler_name} (event: {event_type})
    component._handlers['{handler_name}'] = function(e) {{
        try {{
            {js_body}
        }} catch (error) {{
            console.error('Error in handler {handler_name}:', error);
            console.error('Event:', e);
        }}
    }};
    
    // IMPROVED: Register with all matching elements using data-handler
    // Supports multiple event types: data-handler-click, data-handler-change, etc.
    document.querySelectorAll('[data-handler="{handler_name}"], [data-handler-{event_type}="{handler_name}"]').forEach(el => {{
        el.addEventListener('{event_type}', component._handlers['{handler_name}'].bind(component));
    }});
"""
    
    script += """
})();
"""
    return script


def convert_handler_attributes_in_html(html: str, handlers: Dict[str, str], state_keys: Optional[List[str]] = None) -> str:
    """
    Convert onClick/onChange/etc. attributes from JSX to data-handler format.
    
    IMPROVED: Supports multiple event types, create_on utilities, and inline lambda handlers.
    Also adds data bindings for state variables.
    
    Converts:
    - onClick={handle_increment} -> data-handler-click="handle_increment"
    - create_onclick={handle_increment} -> data-handler-click="handle_increment"
    - onClick={lambda: ...} -> data-handler-click="lambda_handler_123"
    - onChange={handle_change} -> data-handler-change="handle_change"
    - on{EventName}={handler} -> data-handler-{eventname}="handler"
    - {variable} -> data-bind="textContent:state_key"
    """
        
    # Pattern 1: onClick={handler_name} (JSX format)
    # Matches: onClick, onChange, onSubmit, onFocus, onBlur, onMouseEnter, onclick, onchange, etc.
    jsx_pattern = r'\bon([A-Za-z][a-zA-Z0-9]*)\s*=\s*\{(\w+)\}'
    
    def replace_jsx_event_handler(match):
        event_name = match.group(1).lower()  # "Click" -> "click", "click" -> "click"
        handler_name = match.group(2)
        
        # Only replace if it's a known handler
        if handler_name in handlers:
            # Return data-handler attribute with event type and default onclick behavior
            return f'data-handler-{event_name}="{handler_name}" on{event_name.capitalize()}="return false;"'
        return match.group(0)
    
    html = re.sub(jsx_pattern, replace_jsx_event_handler, html)
    
    # Pattern 1b: onClick="handler_name" (HTML format from PSX)
    # Matches: onClick="handler", onChange="handler", onclick="handler", etc.
    html_pattern = r'\bon([A-Za-z][a-zA-Z0-9]*)\s*=\s*"([^"]+)"'
    
    def replace_html_event_handler(match):
        event_name = match.group(1).lower()  # "Click" -> "click", "click" -> "click"
        handler_name = match.group(2)
        
        # Only replace if it's a known handler
        if handler_name in handlers:
            # Return data-handler attribute with event type and default onclick behavior
            return f'data-handler-{event_name}="{handler_name}" on{event_name.capitalize()}="return false;"'
        return match.group(0)
    
    html = re.sub(html_pattern, replace_html_event_handler, html)
    
    # Pattern 1c: create_onclick="python_call_..." or onclick="python_call_..." in rendered HTML
    python_call_pattern = r'\b(?:create_on|on)([A-Za-z][a-zA-Z0-9]*)\s*=\s*"([^"]*python_[^"]*)"'
    
    def replace_python_call_handler(match):
        event_name = match.group(1).lower()
        handler_value = html_module.unescape(match.group(2))
        
        if handler_value in handlers:
            return f'data-handler-{event_name}="{handler_value}" on{event_name.capitalize()}="return false;"'
        return match.group(0)
    
    html = re.sub(python_call_pattern, replace_python_call_handler, html)
    # Matches: create_onclick, create_onchange, create_onsubmit, etc.
    create_on_pattern = r'\bcreate_on([a-z]+)\s*=\s*\{(\w+)\}'
    
    def replace_create_on_handler(match):
        event_name = match.group(1)  # "click", "change", etc.
        handler_name = match.group(2)
        
        # Only replace if it's a known handler
        if handler_name in handlers:
            # Return data-handler attribute with event type and default onclick behavior
            return f'data-handler-{event_name}="{handler_name}" on{event_name.capitalize()}="return false;"'
        return match.group(0)
    
    html = re.sub(create_on_pattern, replace_create_on_handler, html)
    
    # Pattern 3: onClick={lambda ...} (inline lambda handlers)
    # Matches: onClick={lambda e: ...}, onclick={lambda e: ...}, etc.
    lambda_pattern = r'\bon([A-Za-z][a-zA-Z0-9]*)\s*=\s*\{(lambda[^}]+)\}'
    
    def replace_lambda_handler(match):
        event_name = match.group(1).lower()  # "Click" -> "click", "click" -> "click"
        lambda_code = match.group(2).strip()
        
        # Generate unique handler name
        handler_name = f"lambda_handler_{abs(hash(lambda_code))}"
        
        # Convert lambda to JavaScript if not already in handlers
        if handler_name not in handlers:
            try:
                js_code = python_code_to_js(lambda_code, state_keys)
                handlers[handler_name] = js_code
            except Exception as e:
                # If conversion fails, keep original
                return match.group(0)
        
        # Return data-handler attribute
        return f'data-handler-{event_name}="{handler_name}" on{event_name.capitalize()}="return false;"'
    
    html = re.sub(lambda_pattern, replace_lambda_handler, html)
    
    # Pattern 4: create_onclick={lambda ...} (create_on with inline lambda)
    create_lambda_pattern = r'\bcreate_on([a-z]+)\s*=\s*\{(lambda[^}]+)\}'
    
    def replace_create_lambda_handler(match):
        event_name = match.group(1)  # "click", "change", etc.
        lambda_code = match.group(2).strip()
        
        # Generate unique handler name
        handler_name = f"create_lambda_handler_{abs(hash(lambda_code))}"
        
        # Convert lambda to JavaScript if not already in handlers
        if handler_name not in handlers:
            try:
                js_code = python_code_to_js(lambda_code, state_keys)
                handlers[handler_name] = js_code
            except Exception as e:
                # If conversion fails, keep original
                return match.group(0)
        
        # Return data-handler attribute
        return f'data-handler-{event_name}="{handler_name}" on{event_name.capitalize()}="return false;"'
    
    html = re.sub(create_lambda_pattern, replace_create_lambda_handler, html)
    
    # Pattern 5: Add data bindings for state variables
    if state_keys:
        for state_key in state_keys:
            # Find {state_key} patterns and add data binding
            pattern = rf'\{{\s*{state_key}\s*\}}'
            def add_binding(match):
                # Generate unique ID for this binding
                binding_id = f"bind_{state_key}_{abs(hash(match.group(0)))}"
                return f'<span id="{binding_id}" data-bind="textContent:{state_key}">{{{state_key}}}</span>'
            
            html = re.sub(pattern, add_binding, html)
    
    # Pattern 6: data-event="click:handler_name" format (alternative syntax)
    # This allows more flexible specification if developer uses this pattern
    
    return html


# Import after defining helper functions
from ..components.component import component as base_component
from .integration import hydrate_component, get_component_hydrator


def interactive_component(func: Callable) -> Callable:
    """
    Decorator for interactive PSX components with client-side state management.
    
    Properly handles named event handler functions and converts them to JavaScript.
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # First, get the component from the base decorator
        base_component_result = base_component(func)(*args, **kwargs)
        
        # Extract props if provided
        props = args[0] if args and isinstance(args[0], dict) else kwargs
        
        # Extract named handler functions from the component
        # Since the function might be wrapped by JSX transformer, extract from file content
        handlers = {}
        try:
            # Try to get the original file path from the module
            file_path = None
            if hasattr(func, '__module__') and func.__module__ in sys.modules:
                module = sys.modules[func.__module__]
                if hasattr(module, '__original_file__'):
                    file_path = module.__original_file__
            
            # Fallback to inspect.getfile if original file not found
            if not file_path:
                file_path = inspect.getfile(func)
            
            print(f"DEBUG: Extracting handlers from {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            component_pattern = re.compile(rf'^\s*def\s+{re.escape(func.__name__)}\s*\([^)]*\)\s*:')
            component_start = None
            component_indent = 0
            for index, line in enumerate(lines):
                comp_match = component_pattern.match(line)
                if comp_match:
                    component_start = index
                    component_indent = len(line) - len(line.lstrip(' '))
                    break
            
            if component_start is not None:
                i = component_start + 1
                while i < len(lines):
                    line = lines[i]
                    if not line.strip():
                        i += 1
                        continue
                    line_indent = len(line) - len(line.lstrip(' '))
                    if line_indent <= component_indent:
                        break
                    match = re.match(r'^(\s+)def\s+((?:handle|on)_\w+)\s*\([^)]*\)\s*:', line)
                    if match:
                        indent = len(match.group(1))
                        func_name = match.group(2)
                        func_lines = []
                        i += 1
                        while i < len(lines):
                            next_line = lines[i]
                            if not next_line.strip():
                                func_lines.append('')
                                i += 1
                                continue
                            next_indent = len(next_line) - len(next_line.lstrip(' '))
                            if next_indent <= indent:
                                break
                            if next_indent >= indent + 4:
                                func_lines.append(next_line[indent + 4:])
                            else:
                                func_lines.append(next_line.lstrip(' '))
                            i += 1
                        body = '\n'.join(func_lines).rstrip()
                        if body:
                            handlers[func_name] = body
                    else:
                        i += 1
            
            print(f"DEBUG: Found {len(handlers)} handlers: {list(handlers.keys())}")
        except Exception as e:
            print(f"DEBUG: Exception in handler extraction: {e}")
            handlers = {}
        
        if not handlers:
            try:
                handlers = extract_handler_functions(func)
                print(f"DEBUG: Fallback found {len(handlers)} handlers: {list(handlers.keys())}")
            except Exception as e:
                print(f"DEBUG: Fallback exception in handler extraction: {e}")
                handlers = {}
        
        # Extract handlers using new AST-based compiler
        try:
            from ..compiler.handler_compiler import extract_handlers_compiled
            ast_handlers = extract_handlers_compiled(func, func.__name__)
            if ast_handlers:
                handlers.update(ast_handlers)
                print(f"DEBUG: Added AST-based handlers: {list(ast_handlers.keys())}")
        except Exception as e:
            print(f"DEBUG: Failed AST-based handler extraction: {e}")
            # Fallback to old method
            try:
                create_handlers, _ = extract_create_handler_assignments(func, handlers)
                if create_handlers:
                    handlers.update(create_handlers)
                    print(f"DEBUG: Fallback added create_on handlers: {list(create_handlers.keys())}")
            except Exception as e2:
                print(f"DEBUG: Fallback handler extraction failed: {e2}")
        
        # Get the HTML output with interactive handler context
        if hasattr(base_component_result, 'to_html'):
            # Check if this is a PSX element with context
            if hasattr(base_component_result, '_psx_context'):
                # Add interactive handlers to the context for PSX runtime processing
                base_component_result._psx_context['_interactive_handlers'] = {name: True for name in handlers.keys()}
                html = base_component_result.to_html(base_component_result._psx_context)
            else:
                html = base_component_result.to_html()
        else:
            html = str(base_component_result)
        
        # Extract state keys from the component for better conversion
        try:
            source = inspect.getsource(func)
            # Match useState patterns to get state variable names
            state_pattern = r'\[(\w+),\s*set\w+\]\s*=\s*useState'
            state_keys = re.findall(state_pattern, source)
        except (OSError, TypeError):
            state_keys = []
        
        # Convert handler attributes to data-handler attributes with dynamic targeting
        html = convert_handler_attributes_in_html(html, handlers, state_keys)
        
        # Get engine first to generate consistent component ID
        from .engine import get_hydration_engine
        engine = get_hydration_engine()
        component_id = engine.generate_component_id()
        
        # Register component with the generated ID
        from .integration import get_component_hydrator
        hydrator = get_component_hydrator()
        
        # Manually register component to ensure consistent ID
        metadata = hydrator.extract_component_metadata(func)
        component_data = {
            'name': metadata['name'],
            'state': metadata['state'],
            'handlers': metadata['handlers'],
            'effects': metadata['effects'],
            'props': props or {},
        }
        # Override the generated ID with our consistent one
        original_id = engine.register_component(component_data)
        engine.contexts[component_id] = engine.contexts[original_id]
        del engine.contexts[original_id]
        
        # Wrap HTML with hydration data using consistent ID
        state = metadata['state']
        hydrated_html = engine.generate_html_wrapper(component_id, html, state)
        
        # Generate scripts
        full_script = engine.generate_hydration_script()
        handler_script = generate_handler_registration_script(handlers, component_id, state_keys=state_keys)
        hydration_script = hydrator.generate_hydration_script()
        
        # Combine all scripts in correct order
        # 1. Full runtime script (defines NextPyRuntime)
        # 2. Hydration script (initializes components)
        # 3. Handler registration script (uses NextPyRuntime)
        complete_script = f"{full_script}\n\n{hydration_script}\n\n{handler_script}"
        
        # Create a wrapped result that includes hydration data
        class InteractiveComponentResult:
            def __init__(self, html, script):
                self.html = html
                self.script = script
                self.is_interactive = True
            
            def to_html(self, context=None):
                # Embed the full script in the HTML
                return f"{self.html}\n<script type='text/javascript'>\n{self.script}\n</script>"
            
            def __str__(self):
                return f"{self.html}\n<script type='text/javascript'>\n{self.script}\n</script>"
        
        return InteractiveComponentResult(hydrated_html, complete_script)
    
    return wrapper


def enable_hydration_globally():
    """
    Enable hydration globally by replacing the default @component decorator
    """
    import sys
    from .. import components
    
    # Replace component decorator
    original_component = components.component
    
    def hydrated_component(func):
        # Use interactive_component for all components
        return interactive_component(func)
    
    components.component = hydrated_component
    
    print("✓ Global hydration enabled - all @component decorated functions will be interactive")


# HTML template for embedding hydration script and styles
HYDRATION_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* NextPy Hydration Styles */
        .nextpy-component {{
            position: relative;
        }}
        
        .nextpy-component [data-bind] {{
            transition: all 0.3s ease-in-out;
        }}
        
        .nextpy-state-changed {{
            animation: stateChanged 0.3s ease-in-out;
        }}
        
        @keyframes stateChanged {{
            0% {{ opacity: 0.8; }}
            100% {{ opacity: 1; }}
        }}
    </style>
</head>
<body>
    <div id="app">
        {body}
    </div>
    
    <script type="text/javascript">
        {script}
    </script>
</body>
</html>
'''


def create_interactive_page(html: str, script: str, title: str = "NextPy App") -> str:
    """
    Create a complete interactive HTML page
    
    Args:
        html: Component HTML
        script: Hydration script
        title: Page title
        
    Returns:
        Complete HTML page as string
    """
    page = HYDRATION_TEMPLATE.format(
        title=title,
        body=html,
        script=script
    )
    return page
