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
            # Use SHA256 to match _create_python_call_placeholder in component.py
            digest = hashlib.sha256(normalized.encode('utf-8')).hexdigest()[:16]
            return f"python_call_lambda_{digest}"
        except Exception:
            return f"python_call_lambda_{hashlib.sha256(ast.dump(arg).encode()).hexdigest()[:16]}"

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
        print(f"DEBUG extract_create_handler_assignments: Got source, length={len(source)}")
    except (OSError, TypeError) as e:
        print(f"DEBUG extract_create_handler_assignments: Could not get source: {e}")
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
        print(f"DEBUG extract_create_handler_assignments: AST parsed successfully")
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
                    continue

                target_name = node.targets[0].id
                value = node.value

                if isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
                    func_name = value.func.id
                    print(f"DEBUG extract_create_handler_assignments: Found call to {func_name}")
                    if func_name.startswith('create_on') and value.args:
                        event_name = func_name[len('create_on'):].lower()
                        arg = value.args[0]
                        print(f"DEBUG extract_create_handler_assignments: Processing {func_name} with arg type {type(arg).__name__}")

                        if isinstance(arg, ast.Lambda):
                            try:
                                handler_body = ast.unparse(arg.body).strip()
                                placeholder = _get_python_call_placeholder_from_ast(arg)
                                if handler_body:
                                    handlers[target_name] = handler_body
                                    handlers[placeholder] = handler_body
                                    event_types[target_name] = event_name
                                    event_types[placeholder] = event_name
                                    print(f"DEBUG extract_create_handler_assignments: Added placeholder {placeholder} for {target_name}")
                            except Exception as e:
                                print(f"DEBUG extract_create_handler_assignments: Lambda extraction failed: {e}")
                                continue
                        elif isinstance(arg, ast.Name):
                            # The handler function is defined elsewhere
                            placeholder = _get_python_call_placeholder_from_ast(arg)
                            event_types[target_name] = event_name
                            event_types[placeholder] = event_name
                            if existing_handlers and arg.id in existing_handlers:
                                handlers[placeholder] = existing_handlers[arg.id]
                                print(f"DEBUG extract_create_handler_assignments: Added placeholder {placeholder} for named handler {arg.id}")
    except Exception as e:
        print(f"DEBUG extract_create_handler_assignments: AST parsing failed: {e}")
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
        expression = match.group(2)   # The argument
        state_key = setter_name[0].lower() + setter_name[1:]  # "count"
        
        # SAFER: Only do basic state variable replacement
        # Do NOT try to parse full expressions with regex
        expr_js = expression.strip()
        expr_js = replace_state_variables(expr_js, state_keys)
        
        return f"this.stateManager.set('{state_key}', {expr_js})"
    
    # Find all setXxxx(...) calls - SAFER regex without nested parens
    # This pattern matches setName(arg) where arg is a simple expression
    js_code = re.sub(
        r'set([A-Z]\w*)\s*\(([^)]+)\)',
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
    state_keys: Optional[List[str]] = None,
    html: Optional[str] = None
) -> str:
    """
    Generate JavaScript to register all handlers for a component.
    
    IMPROVED: Supports multiple event types and dynamic binding.
    
    Args:
        handlers: {handler_name: handler_code}
        component_id: Component ID for scoping
        event_types: Optional {handler_name: 'click'|'change'|'submit'...}
        state_keys: Optional list of state variable names for better conversion
        html: Optional HTML string to extract python_call_lambda_* placeholders from
    """
    if not handlers:
        return ""
    
    # DEBUG: Log all handlers being registered
    print(f"DEBUG generate_handler_registration_script: handlers keys = {list(handlers.keys())}")
    
    # Extract actual python_call_lambda_* placeholders from HTML
    # These are the placeholders that were generated by the PSX renderer
    # We need to use these exact placeholders as keys in the handlers dict
    import re
    html_placeholders = list(set(re.findall(r'python_call_lambda_[a-f0-9]+', html)))  # Deduplicate
    print(f"DEBUG: Extracted placeholders from HTML: {html_placeholders}")
    
    # Create python_call_lambda_* placeholders for all handlers
    # This ensures the HTML placeholders match the handlers dict
    import hashlib
    handlers_with_placeholders = {}
    for handler_name, handler_code in handlers.items():
        handlers_with_placeholders[handler_name] = handler_code
        
        # Convert list-based handlers to JavaScript strings for placeholder creation
        handler_str = None
        if isinstance(handler_code, str):
            handler_str = handler_code
        elif isinstance(handler_code, list) and handler_code:
            if hasattr(handler_code[0], 'to_dict'):
                # New AST-based structured Action objects
                serialized_actions = [action.to_dict() for action in handler_code]
                handler_str = f"executeNextPyActions({json.dumps(serialized_actions)}, componentId)"
            else:
                # Plain dict actions
                handler_str = f"executeNextPyActions({json.dumps(handler_code)}, componentId)"
        
        # Use the actual placeholder from HTML if available, otherwise create one
        if html_placeholders and handler_str:
            # Use the first available unique placeholder from HTML
            placeholder = html_placeholders.pop(0)
            handlers_with_placeholders[placeholder] = handler_str
            if event_types:
                event_types[placeholder] = event_types.get(handler_name, 'click')
            print(f"DEBUG: Using HTML placeholder {placeholder} for handler {handler_name}")
        elif handler_str:
            # Fallback: create a new placeholder
            placeholder = "python_call_lambda_" + hashlib.sha256(handler_str.encode()).hexdigest()[:16]
            handlers_with_placeholders[placeholder] = handler_str
            if event_types:
                event_types[placeholder] = event_types.get(handler_name, 'click')
            print(f"DEBUG: Created fallback placeholder {placeholder} for handler {handler_name}")
        else:
            print(f"DEBUG: Could not create string representation for handler {handler_name}, type: {type(handler_code)}")
    
    print(f"DEBUG: Final handlers dict keys: {list(handlers_with_placeholders.keys())}")
    
    # Use the expanded handlers dict
    handlers = handlers_with_placeholders
    
    # Default event type is 'click'
    if event_types is None:
        event_types = {name: 'click' for name in handlers}
    
    script = f"""
// Handler registration for component: {component_id}
(function() {{
    // Store handlers on the component
    window.nextpyComponents = window.nextpyComponents || {{}};
    const componentId = '{component_id}';
    
    // Wait for component to be registered (polling approach)
    function registerHandlers() {{
        const component = window.nextpyComponents[componentId];
        
        if (!component) {{
            // Component not yet registered, retry after short delay
            setTimeout(registerHandlers, 50);
            return;
        }}
        
        // Component found, register handlers
        component._handlers = component._handlers || {{}};
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
        
        # Wrap js_body in IIFE for safety to prevent broken injection
        safe_js_body = f"""
(() => {{
    try {{
        {js_body}
    }} catch (innerError) {{
        console.error('Inner error in handler {handler_name}:', innerError);
        throw innerError;
    }}
}})();
"""
        
        # Create the handler function with error handling
        script += f"""
    // Handler: {handler_name} (event: {event_type})
    component._handlers['{handler_name}'] = function(e) {{
        console.log('Handler called: {handler_name}');
        try {{
            {safe_js_body}
        }} catch (error) {{
            console.error('Error in handler {handler_name}:', error);
            console.error('Event:', e);
        }}
    }};
"""
    
    
    # Add global event delegation system
    script += """
    // Global event delegation system - handles all events dynamically
    function setupEventDelegation() {
        // Delegate click events
        document.addEventListener('click', function(e) {
            console.log('Click detected on:', e.target);
            const el = e.target.closest('[data-handler-click]');
            console.log('Found data-handler-click element:', el);
            if (!el) return;

            const handlerName = el.getAttribute('data-handler-click');
            console.log('Handler name:', handlerName);
            
            // Fallback component ID lookup - try multiple sources
            let componentId = el.closest('[data-component-id]')?.getAttribute('data-component-id');
            console.log('Component ID from element:', componentId);
            if (!componentId) {
                componentId = document.body.getAttribute('data-component-id');
                console.log('Component ID from body:', componentId);
            }
            if (!componentId) {
                const componentIds = Object.keys(window.nextpyComponents || {});
                console.log('Available component IDs:', componentIds);
                if (componentIds.length > 0) {
                    componentId = componentIds[0];
                }
            }
            
            if (!componentId) return;

            const component = window.nextpyComponents?.[componentId];
            console.log('Component found:', component);
            if (!component) return;

            const handler = component._handlers?.[handlerName];
            console.log('Handler found:', handler);
            if (handler) handler.call(component, e);
        });

        // Delegate change events
        document.addEventListener('change', function(e) {
            const el = e.target.closest('[data-handler-change]');
            if (!el) return;

            const handlerName = el.getAttribute('data-handler-change');
            
            // Fallback component ID lookup
            let componentId = el.closest('[data-component-id]')?.getAttribute('data-component-id');
            if (!componentId) {
                componentId = document.body.getAttribute('data-component-id');
            }
            if (!componentId) {
                const componentIds = Object.keys(window.nextpyComponents || {});
                if (componentIds.length > 0) {
                    componentId = componentIds[0];
                }
            }
            
            if (!componentId) return;

            const component = window.nextpyComponents?.[componentId];
            if (!component) return;

            const handler = component._handlers?.[handlerName];
            if (handler) handler.call(component, e);
        });

        // Delegate submit events
        document.addEventListener('submit', function(e) {
            const el = e.target.closest('[data-handler-submit]');
            if (!el) return;

            const handlerName = el.getAttribute('data-handler-submit');
            
            // Fallback component ID lookup
            let componentId = el.closest('[data-component-id]')?.getAttribute('data-component-id');
            if (!componentId) {
                componentId = document.body.getAttribute('data-component-id');
            }
            if (!componentId) {
                const componentIds = Object.keys(window.nextpyComponents || {});
                if (componentIds.length > 0) {
                    componentId = componentIds[0];
                }
            }
            
            if (!componentId) return;

            const component = window.nextpyComponents?.[componentId];
            if (!component) return;

            const handler = component._handlers?.[handlerName];
            if (handler) {
                e.preventDefault();
                handler.call(component, e);
            }
        });
    }

    // Setup event delegation once
    if (!window.__nextpyEventDelegationSetup) {
        setupEventDelegation();
        window.__nextpyEventDelegationSetup = true;
    }
    }
    
    // Start polling for component registration
    registerHandlers();
"""
    
    script += """
})();
"""
    return script


def convert_handler_attributes_in_html(html: str, handlers: Dict[str, str], state_keys: Optional[List[str]] = None, initial_state: Optional[Dict[str, Any]] = None) -> str:
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
    print(f"DEBUG convert_handler_attributes_in_html: Input HTML length={len(html)}, handlers={list(handlers.keys())}, state_keys={state_keys}")
    
    # DEBUG: Show sample of HTML with create_on attributes
    import re
    create_on_samples = re.findall(r'create_on\w+\s*=\s*[^>]+', html[:1000])
    print(f"DEBUG: Found create_on patterns in HTML: {create_on_samples}")
    
    # DEBUG: Show actual button HTML
    button_samples = re.findall(r'<button[^>]*create_on[^>]*>.*?</button>', html[:1000], re.DOTALL)
    print(f"DEBUG: Button HTML samples: {button_samples[:2] if button_samples else 'None'}")
    
    # DEBUG: Show state variable patterns in HTML
    state_var_samples = re.findall(r'\{[a-zA-Z_][a-zA-Z0-9_]*\}', html[:1000])
    print(f"DEBUG: Found state variable patterns: {state_var_samples}")

    # DEBUG: Show actual HTML content around state variables
    count_samples = re.findall(r'[^>]*count[^<]*', html[:1000], re.IGNORECASE)
    print(f"DEBUG: HTML samples with 'count': {count_samples[:3] if count_samples else 'None'}")
        
    # Pattern 1: onClick={handler_name} (JSX format)
    # Matches: onClick, onChange, onSubmit, onFocus, onBlur, onMouseEnter, onclick, onchange, etc.
    jsx_pattern = r'\bon([A-Za-z][a-zA-Z0-9]*)\s*=\s*\{(\w+)\}'
    
    def replace_jsx_event_handler(match):
        event_name = match.group(1).lower()  # "Click" -> "click", "click" -> "click"
        handler_name = match.group(2)
        
        # Only replace if it's a known handler
        if handler_name in handlers:
            # Return ONLY data-handler attribute - NO onclick
            return f'data-handler-{event_name}="{handler_name}"'
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
            # Return ONLY data-handler attribute - NO onclick
            return f'data-handler-{event_name}="{handler_name}"'
        return match.group(0)
    
    html = re.sub(html_pattern, replace_html_event_handler, html)
    
    # Pattern 1c: create_onclick="python_call_..." or onclick="python_call_..." in rendered HTML
    # ALWAYS convert these to data-handler format regardless of handlers dict
    python_call_pattern = r'(?:create_on|on)([A-Za-z][a-zA-Z0-9]*)\s*=\s*"([^"]*python_call_lambda_[^"]*)"'
    
    def replace_python_call_handler(match):
        event_name = match.group(1).lower()
        handler_value = html_module.unescape(match.group(2))
        
        replacement = f'data-handler-{event_name}="{handler_value}"'
        print(f"DEBUG: python_call pattern matched: event={event_name}, handler={handler_value}, replacement={replacement}")
        
        # ALWAYS convert to data-handler - don't check if in handlers dict
        # The python_call_lambda_* placeholders will be resolved at runtime
        return replacement
    
    html = re.sub(python_call_pattern, replace_python_call_handler, html)
    print(f"DEBUG: After python_call pattern, HTML contains create_on: {'create_on' in html}")
    
    # Matches: create_onclick, create_onchange, create_onsubmit, etc.
    create_on_pattern = r'\bcreate_on([a-z]+)\s*=\s*\{(\w+)\}'
    
    def replace_create_on_handler(match):
        event_name = match.group(1)  # "click", "change", etc.
        handler_name = match.group(2)
        
        print(f"DEBUG: create_on pattern matched: event={event_name}, handler={handler_name}")
        
        # Only replace if it's a known handler
        if handler_name in handlers:
            # Return ONLY data-handler attribute - NO onclick
            return f'data-handler-{event_name}="{handler_name}"'
        return match.group(0)
    
    html = re.sub(create_on_pattern, replace_create_on_handler, html)
    print(f"DEBUG: After create_on pattern, HTML contains create_on: {'create_on' in html}")
    
    # Pattern 2b: create_onclick={lambda ...} (inline lambda with create_on)
    create_lambda_pattern = r'\bcreate_on([a-z]+)\s*=\s*\{(lambda[^}]+)\}'
    
    def replace_create_lambda_handler(match):
        event_name = match.group(1)  # "click", "change", etc.
        lambda_code = match.group(2).strip()
        
        print(f"DEBUG: create_on lambda pattern matched: event={event_name}, lambda={lambda_code[:50]}")
        
        # Generate stable handler name using SHA256 to match component.py
        handler_name = "create_lambda_" + hashlib.sha256(lambda_code.encode()).hexdigest()[:10]
        
        # Convert lambda to JavaScript if not already in handlers
        if handler_name not in handlers:
            try:
                js_code = python_code_to_js(lambda_code, state_keys)
                handlers[handler_name] = js_code
                print(f"DEBUG: Added create_lambda handler: {handler_name}")
            except Exception as e:
                # If conversion fails, keep original
                print(f"DEBUG: create_lambda conversion failed: {e}")
                return match.group(0)
        
        # Return ONLY data-handler attribute - NO onclick
        return f'data-handler-{event_name}="{handler_name}"'
    
    html = re.sub(create_lambda_pattern, replace_create_lambda_handler, html)
    print(f"DEBUG: After create_lambda pattern, HTML contains create_on: {'create_on' in html}")
    
    # Pattern 2c: create_onclick="&lt;lambda&gt;" (HTML-escaped lambda)
    # This handles the case where _create_python_call_placeholder returns "<lambda>" which gets HTML-escaped
    create_on_lambda_escaped_pattern = r'\bcreate_on([a-z]+)\s*=\s*"&lt;lambda&gt;"'
    
    def replace_create_on_lambda_escaped(match):
        event_name = match.group(1)  # "click", "change", etc.
        
        print(f"DEBUG: create_on lambda escaped pattern matched: event={event_name}")
        
        # Generate a unique placeholder for this lambda
        # Since we don't have the lambda code, we'll use a counter
        handler_name = f"python_call_lambda_{hashlib.sha256(event_name.encode()).hexdigest()[:10]}"
        
        # Return data-handler attribute
        return f'data-handler-{event_name}="{handler_name}"'
    
    html = re.sub(create_on_lambda_escaped_pattern, replace_create_on_lambda_escaped, html)
    print(f"DEBUG: After create_on lambda escaped pattern, HTML contains create_on: {'create_on' in html}")
    
    # Pattern 3: onClick={lambda ...} (inline lambda handlers)
    # Matches: onClick={lambda e: ...}, onclick={lambda e: ...}, etc.
    lambda_pattern = r'\bon([A-Za-z][a-zA-Z0-9]*)\s*=\s*\{(lambda[^}]+)\}'
    
    def replace_lambda_handler(match):
        event_name = match.group(1).lower()  # "Click" -> "click", "click" -> "click"
        lambda_code = match.group(2).strip()
        
        # Generate stable handler name using SHA256 to match component.py
        handler_name = "lambda_" + hashlib.sha256(lambda_code.encode()).hexdigest()[:10]
        
        # Convert lambda to JavaScript if not already in handlers
        if handler_name not in handlers:
            try:
                js_code = python_code_to_js(lambda_code, state_keys)
                handlers[handler_name] = js_code
            except Exception as e:
                # If conversion fails, keep original
                return match.group(0)
        
        # Return ONLY data-handler attribute - NO onclick
        return f'data-handler-{event_name}="{handler_name}"'
    
    html = re.sub(lambda_pattern, replace_lambda_handler, html)
    
    # Pattern 4: create_onclick={lambda ...} (create_on with inline lambda)
    create_lambda_pattern = r'\bcreate_on([a-z]+)\s*=\s*\{(lambda[^}]+)\}'
    
    def replace_create_lambda_handler(match):
        event_name = match.group(1)  # "click", "change", etc.
        lambda_code = match.group(2).strip()
        
        # Generate stable handler name using SHA256 to match component.py
        handler_name = "create_lambda_" + hashlib.sha256(lambda_code.encode()).hexdigest()[:10]
        
        # Convert lambda to JavaScript if not already in handlers
        if handler_name not in handlers:
            try:
                js_code = python_code_to_js(lambda_code, state_keys)
                handlers[handler_name] = js_code
            except Exception as e:
                # If conversion fails, keep original
                return match.group(0)
        
        # Return ONLY data-handler attribute - NO onclick
        return f'data-handler-{event_name}="{handler_name}"'
    
    html = re.sub(create_lambda_pattern, replace_create_lambda_handler, html)
    
    # Pattern 5: Add data-bind attributes to elements containing state variables
    # Since PSX renderer outputs actual values instead of {state_key} patterns,
    # we match against the actual rendered values from initial_state
    if state_keys and initial_state:
        binding_counter = 0
        for state_key in state_keys:
            state_value = str(initial_state.get(state_key, ''))
            if not state_value:
                continue
            
            # Pattern to find elements containing the state value in their text
            # This adds data-bind attribute to the opening tag
            # More flexible pattern that handles various HTML structures
            pattern = rf'(<(\w+)[^>]*>)([^<]*\b{re.escape(state_value)}\b[^<]*)(</\2>)'
            
            def add_binding_to_element(match):
                nonlocal binding_counter
                opening_tag = match.group(1)
                tag_name = match.group(2)
                text_content = match.group(3)
                closing_tag = match.group(4)
                
                # Check if element already has data-bind
                if 'data-bind=' in opening_tag or 'data-element-id=' in opening_tag:
                    return match.group(0)
                
                # Generate unique element ID for binding
                element_id = f"binding_{state_key}_{binding_counter}"
                binding_counter += 1
                
                # Add data-bind and data-element-id attributes to opening tag
                # Insert before the closing >
                modified_tag = opening_tag.rstrip('>') + f' data-bind="textContent:{state_key}" data-element-id="{element_id}">'
                
                return f'{modified_tag}{text_content}{closing_tag}'
            
            html = re.sub(pattern, add_binding_to_element, html)
            print(f"DEBUG: Added data-bind attribute for state key: {state_key} (value: {state_value})")
    
    # Pattern 6: data-event="click:handler_name" format (alternative syntax)
    # This allows more flexible specification if developer uses this pattern
    
    # FINAL CLEANUP: Remove any remaining create_on attributes that weren't converted
    html = re.sub(r'\s*create_on\w+\s*=\s*"[^"]*"', '', html)
    print(f"DEBUG: After final cleanup, HTML contains create_on: {'create_on' in html}")
    
    # DEBUG: Check if data-bind attributes are in HTML
    data_bind_count = len(re.findall(r'data-bind=', html))
    print(f"DEBUG: HTML contains {data_bind_count} data-bind attributes")
    
    print(f"DEBUG convert_handler_attributes_in_html: Final HTML contains create_on: {'create_on' in html}, contains data-handler: {'data-handler' in html}")
    return html


# Import after defining helper functions
from ..components.component import component as base_component
from .integration import get_component_hydrator


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
            
        except Exception as e:
            print(f"DEBUG: Exception in handler extraction: {e}")
            handlers = {}
        
        if not handlers:
            try:
                handlers = extract_handler_functions(func)
            except Exception as e:
                print(f"DEBUG: Fallback exception in handler extraction: {e}")
                handlers = {}
        
        # Extract create_on handlers FIRST to get python_call_lambda_* placeholders
        try:
            create_handlers, _ = extract_create_handler_assignments(func, handlers)
            if create_handlers:
                handlers.update(create_handlers)
        except Exception as e:
            print(f"DEBUG: create_on handler extraction failed: {e}")
        
        # Extract handlers using new AST-based compiler
        try:
            from ..compiler.handler_compiler import extract_handlers_compiled
            ast_handlers = extract_handlers_compiled(func, func.__name__)
            if ast_handlers:
                handlers.update(ast_handlers)
        except Exception as e:
            print(f"DEBUG: Failed AST-based handler extraction: {e}")
        
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
        import re
        try:
            # Try to get source from function first
            source = inspect.getsource(func)
            # Match useState patterns to get state variable names
            state_pattern = r'\[(\w+),\s*set\w+\]\s*=\s*useState'
            state_keys = re.findall(state_pattern, source)
            print(f"DEBUG: Extracted state_keys from source: {state_keys}")
        except (OSError, TypeError) as e:
            print(f"DEBUG: Could not extract state_keys from source: {e}")
            # Fallback: try to read from PSX file using the same logic as EnhancedHandlerExtractor
            try:
                # Get the module name from the function
                module = inspect.getmodule(func)
                if module and module.__name__:
                    module_name = module.__name__.split('.')[-1]
                    # Try to find the PSX file in pages directory
                    import os
                    pages_path = os.path.join(os.getcwd(), 'pages')
                    psx_file = os.path.join(pages_path, f'{module_name}.psx')
                    
                    if os.path.exists(psx_file):
                        with open(psx_file, 'r') as f:
                            source = f.read()
                            state_pattern = r'\[(\w+),\s*set\w+\]\s*=\s*useState'
                            state_keys = re.findall(state_pattern, source)
                            print(f"DEBUG: Extracted state_keys from PSX file: {state_keys}")
                    else:
                        print(f"DEBUG: PSX file not found: {psx_file}")
                        state_keys = []
                else:
                    state_keys = []
            except Exception as e:
                print(f"DEBUG: Could not extract state_keys from file: {e}")
                state_keys = []
        
        print(f"DEBUG: state_keys passed to convert_handler_attributes_in_html: {state_keys}")
        
        # Register component with the generated ID
        from .integration import get_component_hydrator
        hydrator = get_component_hydrator()
        
        # Get initial state for data-bind pattern matching
        metadata = hydrator.extract_component_metadata(func)
        print(f"DEBUG: Extracted metadata state: {metadata['state']}")
        initial_state = metadata['state']
        
        # Convert handler attributes to data-handler attributes with dynamic targeting
        html = convert_handler_attributes_in_html(html, handlers, state_keys, initial_state)
        
        # Get engine first to generate consistent component ID
        from .engine import get_hydration_engine
        engine = get_hydration_engine()
        component_id = engine.generate_component_id()
        
        # Manually register component to ensure consistent ID
        component_data = {
            'name': metadata['name'],
            'state': metadata['state'],
            'handlers': metadata['handlers'],
            'effects': metadata['effects'],
            'props': props or {},
        }
        print(f"DEBUG: Component data state: {component_data['state']}")
        # Override the generated ID with our consistent one
        original_id = engine.register_component(component_data)
        engine.contexts[component_id] = engine.contexts[original_id]
        del engine.contexts[original_id]
        
        # Wrap HTML with hydration data using consistent ID
        state = metadata['state']
        print(f"DEBUG: State passed to generate_html_wrapper: {state}")
        hydrated_html = engine.generate_html_wrapper(component_id, html, state)
        
        # Generate scripts
        full_script = engine.generate_hydration_script()
        handler_script = generate_handler_registration_script(handlers, component_id, state_keys=state_keys, html=html)
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
