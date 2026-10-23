"""
Interactive Component Decorator for NextPy PSX - PRODUCTION VERSION
Enables client-side interactivity with proper handler registration
"""

import sys
import os
import inspect
import re
import ast
import hashlib
import html as html_module
import json
from functools import wraps
from typing import Callable, Dict, Any, Optional, List, Tuple


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
    except (OSError, TypeError) as e:
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
                            except Exception as e:
                                continue
                        elif isinstance(arg, ast.Name):
                            # The handler function is defined elsewhere
                            placeholder = _get_python_call_placeholder_from_ast(arg)
                            event_types[target_name] = event_name
                            event_types[placeholder] = event_name
                            if existing_handlers and arg.id in existing_handlers:
                                handlers[placeholder] = existing_handlers[arg.id]
    except Exception as e:
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
            # Not preceded by quote or dot, not followed by quote or dot or bracket
            (rf'(?<![\'".])\b{potential_key}\b(?!\s*[\.\(\[])(?![\'"])', f'this.stateManager.get(\'{potential_key}\')'),
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
    # Decode HTML entities (e.g., &quot; from data-if-true attributes)
    import html as _html
    js_code = _html.unescape(python_code)
    
    # Convert lambda to direct body: lambda e: expr -> expr
    # This ensures the body executes when the handler is called
    lambda_match = re.match(r'lambda\s+(\w+):(.*)', js_code)
    if lambda_match:
        param = lambda_match.group(1)
        body = lambda_match.group(2)
        # Convert setter calls in the body
        body = re.sub(r'set([A-Z]\w*)\s*\(([^)]+)\)', 
            lambda m: f"this.stateManager.set('{m.group(1)[0].lower() + m.group(1)[1:]}', {m.group(2)})", body)
        body = body.replace('True', 'true').replace('False', 'false').replace('None', 'null')
        body = body.strip()
        js_code = body
    
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

        # Map the setter back to the actual useState variable. This handles
        # setFullName -> full_name and setConfirmingDelete -> confirming_delete.
        normalized_setter = setter_name.replace('_', '').lower()
        for key in (state_keys or []):
            if key == state_key or key.replace('_', '').lower() == normalized_setter:
                state_key = key
                break
        
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
    js_code = re.sub(r'[ \t]+', ' ', js_code)  # Normalize spaces, preserve newlines
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
    
    # Extract placeholders from HTML - these are the correct ones from PSX rendering
    import re
    html_placeholders = re.findall(r'python_call_lambda_[a-f0-9]+', html)
    # Deduplicate while preserving order
    seen = set()
    html_placeholders = [x for x in html_placeholders if not (x in seen or seen.add(x))]
    
    # Convert list-based handlers to JavaScript strings and build a code->handler mapping
    handlers_with_js = {}
    code_to_handler = {}  # Map normalized code to handler name
    
    
    
    for handler_name, handler_code in handlers.items():
        handler_str = None
        if isinstance(handler_code, str):
            handler_str = handler_code
            # Create a normalized version for matching
            normalized_code = re.sub(r'\s+', ' ', handler_code).strip()
            code_to_handler[normalized_code] = handler_name
        elif isinstance(handler_code, list) and handler_code:
            if hasattr(handler_code[0], 'to_dict'):
                # New AST-based structured Action objects
                serialized_actions = [action.to_dict() for action in handler_code]
                handler_str = f"executeNextPyActions({json.dumps(serialized_actions)}, componentId)"
            else:
                # Plain dict actions
                handler_str = f"executeNextPyActions({json.dumps(handler_code)}, componentId)"
        
        if handler_str:
            handlers_with_js[handler_name] = handler_str
    
    # If we have HTML placeholders but handler keys don't match them,
    # we need to map them using name-based matching instead of position-based
    # FIX: Use name-based matching to ensure handlers are correctly identified
    handler_keys_set = set(handlers_with_js.keys())
    html_placeholders_set = set(html_placeholders)
    
    if html_placeholders and not handler_keys_set.issubset(html_placeholders_set):
        # Name-based matching: try to match handler names with placeholders
        handlers_remapped = {}
        for placeholder in html_placeholders:
            # Try to find a handler that matches this placeholder
            if placeholder in handlers_with_js:
                handlers_remapped[placeholder] = handlers_with_js[placeholder]
            else:
                # Try to find a handler by partial name match
                for handler_name in handlers_with_js.keys():
                    # Check if handler_name is contained in placeholder or vice versa
                    if handler_name in placeholder or placeholder in handler_name:
                        handlers_remapped[placeholder] = handlers_with_js[handler_name]
                        break
        
        # If name-based matching failed, fall back to position-based as last resort
        if not handlers_remapped or len(handlers_remapped) != len(html_placeholders):
            handler_names = list(handlers_with_js.keys())
            for i, placeholder in enumerate(html_placeholders):
                if i < len(handler_names) and placeholder not in handlers_remapped:
                    handlers_remapped[placeholder] = handlers_with_js[handler_names[i]]
        
        handlers_with_js = handlers_remapped
    
    # Use the handlers with JavaScript strings
    handlers = handlers_with_js
    
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
        try {{
            const triggerElement = e.__nextpyHandlerElement || e.currentTarget;
            const bridgedEvent = {{
                target: e.target,
                currentTarget: triggerElement,
                type: e.type,
                key: e.key,
                code: e.code,
                detail: e.detail,
                preventDefault: () => e.preventDefault(),
                stopPropagation: () => e.stopPropagation()
            }};
            if (e.target && e.target.dataset) {{
                bridgedEvent.targetDataset = {{ ...e.target.dataset }};
            }}
            if (triggerElement && triggerElement.dataset) {{
                bridgedEvent.currentTargetDataset = {{ ...triggerElement.dataset }};
            }}
            if (e.target && e.target.value !== undefined) {{
                bridgedEvent.value = e.target.value;
            }}
            if (component.state) {{
                component.state.e = bridgedEvent;
                component.state.event = bridgedEvent;
            }}
            const actionRuntime = window.NextPyActionRuntime;
            const actionComponent = actionRuntime && actionRuntime.components && actionRuntime.components.get(componentId);
            if (actionComponent && actionComponent.state) {{
                actionComponent.state.e = bridgedEvent;
                actionComponent.state.event = bridgedEvent;
            }}
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

            const rawHandlerName = el.getAttribute('data-handler-click');
            const handlerName = rawHandlerName ? rawHandlerName.replace(/^[\"']|[\"']$/g, '') : rawHandlerName;
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
            if (handler) { e.__nextpyHandlerElement = el; handler.call(component, e); }
        });

        // Delegate change events
        document.addEventListener('change', function(e) {
            const el = e.target.closest('[data-handler-change]');
            if (!el) return;

            const rawHandlerName = el.getAttribute('data-handler-change');
            const handlerName = rawHandlerName ? rawHandlerName.replace(/^[\"']|[\"']$/g, '') : rawHandlerName;
            
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
            if (handler) { e.__nextpyHandlerElement = el; handler.call(component, e); }
        });

        // Delegate input events (text/password/textarea bindings)
        document.addEventListener('input', function(e) {
            const el = e.target.closest('[data-handler-input]');
            if (!el) return;

            const rawHandlerName = el.getAttribute('data-handler-input');
            const handlerName = rawHandlerName ? rawHandlerName.replace(/^[\"']|[\"']$/g, '') : rawHandlerName;

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
            if (handler) { e.__nextpyHandlerElement = el; handler.call(component, e); }
        });

        // Delegate submit events
        document.addEventListener('submit', function(e) {
            const el = e.target.closest('[data-handler-submit]');
            if (!el) return;

            const rawHandlerName = el.getAttribute('data-handler-submit');
            const handlerName = rawHandlerName ? rawHandlerName.replace(/^[\"']|[\"']$/g, '') : rawHandlerName;
            
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
                e.__nextpyHandlerElement = el;
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
    
    # Pattern 1: onClick={handler_name} (JSX format)
    # Matches: onClick, onChange, onSubmit, onFocus, onBlur, onMouseEnter, onclick, onchange, etc.
    jsx_pattern = r'\bon([A-Za-z][a-zA-Z0-9]*)\s*=\s*\{(\w+)\}'
    
    def replace_jsx_event_handler(match):
        event_name = match.group(1).lower()  # "Click" -> "click", "click" -> "click"
        handler_name = match.group(2)
        
        # Only replace if it's a known handler
        if handler_name in handlers:
            # Use &quot; so the replacement is safe inside data-if-true attribute values
            # getAttribute() auto-decodes HTML entities
            return f'data-handler-{event_name}=&quot;{handler_name}&quot;'
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
            # Use &quot; so the replacement is safe inside data-if-true attribute values
            # getAttribute() auto-decodes HTML entities
            return f'data-handler-{event_name}=&quot;{handler_name}&quot;'
        return match.group(0)
    
    html = re.sub(html_pattern, replace_html_event_handler, html)
    
    # Pattern 1c: create_onclick="python_call_..." or onclick="python_call_..." in rendered HTML
    # ALWAYS convert these to data-handler format regardless of handlers dict
    python_call_pattern = r'(?:create_on|on)([A-Za-z][a-zA-Z0-9]*)\s*=\s*"([^"]*python_call_lambda_[^"]*)"'
    
    def replace_python_call_handler(match):
        event_name = match.group(1).lower()
        handler_value = html_module.unescape(match.group(2))
        
        # Use &quot; so the replacement is safe inside data-if-true attribute values
        replacement = f'data-handler-{event_name}=&quot;{handler_value}&quot;'
        
        # ALWAYS convert to data-handler - don't check if in handlers dict
        # The python_call_lambda_* placeholders will be resolved at runtime
        return replacement
    
    html = re.sub(python_call_pattern, replace_python_call_handler, html)
    
    # Matches: create_onclick, create_onchange, create_onsubmit, etc.
    # Updated to handle placeholder names like python_call_handleSubmit
    create_on_pattern = r'\bcreate_on([a-z]+)\s*=\s*\{([a-zA-Z0-9_]+)\}'
    
    def replace_create_on_handler(match):
        event_name = match.group(1)  # "click", "change", etc.
        handler_name = match.group(2)
        
        # Return data-handler attribute - the handler will be registered separately
        # Use &quot; so the replacement is safe inside data-if-true attribute values
        return f'data-handler-{event_name}=&quot;{handler_name}&quot;'
    
    html = re.sub(create_on_pattern, replace_create_on_handler, html)
    
    # Pattern 2b: create_onclick={lambda ...} (inline lambda with create_on)
    # This pattern should NOT match if the lambda has already been converted to a placeholder
    # Only match actual lambda code, not placeholder names
    create_lambda_pattern = r'\bcreate_on([a-z]+)\s*=\s*\{(lambda\s+[^}]+)\}'
    
    def replace_create_lambda_handler(match):
        event_name = match.group(1)  # "click", "change", etc.
        lambda_code = match.group(2).strip()
        
        # Decode HTML entities that may have been introduced by html.escape()
        import html as _html_mod
        clean_lambda_code = _html_mod.unescape(lambda_code)
        
        # Generate stable handler name using SHA256 to match _render_element_node ([:12])
        handler_name = "create_lambda_" + hashlib.sha256(clean_lambda_code.encode()).hexdigest()[:12]
        
        # Convert lambda to JavaScript if not already in handlers
        if handler_name not in handlers:
            try:
                js_code = python_code_to_js(lambda_code, state_keys)
                handlers[handler_name] = js_code
            except Exception as e:
                # If conversion fails, keep original
                return match.group(0)
        
        # Return ONLY data-handler attribute - NO onclick
        # Use &quot; so the replacement is safe inside data-if-true attribute values
        return f'data-handler-{event_name}=&quot;{handler_name}&quot;'
    
    html = re.sub(create_lambda_pattern, replace_create_lambda_handler, html)
    
    # Pattern 2c: create_onclick="&lt;lambda&gt;" (HTML-escaped lambda)
    # This handles the case where _create_python_call_placeholder returns "<lambda>" which gets HTML-escaped
    create_on_lambda_escaped_pattern = r'\bcreate_on([a-z]+)\s*=\s*"&lt;lambda&gt;"'
    
    def replace_create_on_lambda_escaped(match):
        event_name = match.group(1)  # "click", "change", etc.
        
        # Generate a unique placeholder for this lambda
        # Since we don't have the lambda code, we'll use a counter
        handler_name = f"python_call_lambda_{hashlib.sha256(event_name.encode()).hexdigest()[:10]}"
        
        # Return data-handler attribute
        # Use &quot; so the replacement is safe inside data-if-true attribute values
        return f'data-handler-{event_name}=&quot;{handler_name}&quot;'
    
    html = re.sub(create_on_lambda_escaped_pattern, replace_create_on_lambda_escaped, html)
    
    # Pattern 3: onClick={lambda ...} (inline lambda handlers)
    # Matches: onClick={lambda e: ...}, onclick={lambda e: ...}, etc.
    lambda_pattern = r'\bon([A-Za-z][a-zA-Z0-9]*)\s*=\s*\{(lambda[^}]+)\}'
    
    def replace_lambda_handler(match):
        event_name = match.group(1).lower()  # "Click" -> "click", "click" -> "click"
        lambda_code = match.group(2).strip()
        
        # Decode HTML entities that may have been introduced by html.escape() in data-if-true attributes
        import html as _html_mod
        clean_lambda_code = _html_mod.unescape(lambda_code)
        
        # Generate stable handler name using SHA256 to match _render_element_node ([:12])
        handler_name = "lambda_" + hashlib.sha256(clean_lambda_code.encode()).hexdigest()[:12]
        
        # Convert lambda to JavaScript if not already in handlers
        if handler_name not in handlers:
            try:
                js_code = python_code_to_js(lambda_code, state_keys)
                handlers[handler_name] = js_code
            except Exception as e:
                # If conversion fails, keep original
                return match.group(0)
        
        # Return ONLY data-handler attribute - NO onclick
        # Use &quot; so the replacement is safe inside data-if-true attribute values
        return f'data-handler-{event_name}=&quot;{handler_name}&quot;'
    
    html = re.sub(lambda_pattern, replace_lambda_handler, html)
    
    # Pattern 4: create_onclick={lambda ...} (create_on with inline lambda)
    create_lambda_pattern = r'\bcreate_on([a-z]+)\s*=\s*\{(lambda[^}]+)\}'
    
    def replace_create_lambda_handler(match):
        event_name = match.group(1)  # "click", "change", etc.
        lambda_code = match.group(2).strip()
        
        # Decode HTML entities that may have been introduced by html.escape()
        import html as _html_mod
        clean_lambda_code = _html_mod.unescape(lambda_code)
        
        # Generate stable handler name using SHA256 to match _render_element_node ([:12])
        handler_name = "create_lambda_" + hashlib.sha256(clean_lambda_code.encode()).hexdigest()[:12]
        
        # Convert lambda to JavaScript if not already in handlers
        if handler_name not in handlers:
            try:
                js_code = python_code_to_js(lambda_code, state_keys)
                handlers[handler_name] = js_code
            except Exception as e:
                # If conversion fails, keep original
                return match.group(0)
        
        # Return ONLY data-handler attribute - NO onclick
        # Use &quot; so the replacement is safe inside data-if-true attribute values
        return f'data-handler-{event_name}=&quot;{handler_name}&quot;'
    
    html = re.sub(create_lambda_pattern, replace_create_lambda_handler, html)
    
    # Pattern 5: Add data-bind attributes to state values in HTML
    # Replace state values with spans containing data-bind attributes
    # This preserves surrounding static text
    if state_keys and initial_state:
        # First, protect all HTML attribute values to prevent wrapping inside attributes
        # Store them in a dictionary with unique placeholders
        protected_attrs = {}
        attr_placeholder_counter = 0

        def protect_attr_values(match):
            nonlocal attr_placeholder_counter
            attr_value = match.group(1)  # Get the captured value inside quotes
            placeholder = f"__ATTR_PLACEHOLDER_{attr_placeholder_counter}__"
            protected_attrs[placeholder] = attr_value
            attr_placeholder_counter += 1
            return placeholder

        # Protect all attribute values (anything between quotes after =)
        # Use separate patterns for double and single quotes to handle them correctly
        html = re.sub(r'=\s*"([^"]*)"', lambda m: '="' + protect_attr_values(m) + '"', html)
        html = re.sub(r"=\s*'([^']*)'", lambda m: "='" + protect_attr_values(m) + "'", html)

        # Now apply data-binding wrapping to the remaining content (which is not inside attributes)
        for state_key in state_keys:
            state_value = initial_state.get(state_key, '')
            if state_value is None or state_value == '':
                continue

            # Handle different value types appropriately
            if isinstance(state_value, (list, dict)):
                # For complex types, use JSON serialization for the pattern
                import json
                state_value_str = json.dumps(state_value)
                binding_type = 'innerHTML'  # Use innerHTML for complex types
            else:
                state_value_str = str(state_value)
                binding_type = 'textContent'

            # Replace the state value with a span containing data-bind attribute
            pattern = rf'\b{re.escape(state_value_str)}\b'

            def wrap_value_with_binding(match):
                value = match.group(0)
                return f'<span data-bind="{binding_type}:{state_key}">{value}</span>'

            html = re.sub(pattern, wrap_value_with_binding, html)

        # Restore the protected attribute values
        for placeholder, original_attr in protected_attrs.items():
            html = html.replace(placeholder, original_attr)
    
    # Pattern 6: data-event="click:handler_name" format (alternative syntax)
    # This allows more flexible specification if developer uses this pattern
    
    # FINAL CLEANUP: Remove any remaining create_on attributes that weren't converted
    html = re.sub(r'\s*create_on\w+\s*=\s*"[^"]*"', '', html)
    
    return html


# Import after defining helper functions
from ..components.component import component as base_component
from .integration import get_component_hydrator


def _get_component_source(func: Callable) -> str:
    """Return the best available Python source for a component function."""
    candidates = []
    try:
        if hasattr(func, '__module__') and func.__module__ in sys.modules:
            module = sys.modules[func.__module__]
            if hasattr(module, '__original_file__'):
                candidates.append(module.__original_file__)
    except Exception:
        pass
    try:
        code_file = getattr(getattr(func, '__code__', None), 'co_filename', None)
        if code_file:
            candidates.append(code_file)
    except Exception:
        pass
    try:
        candidates.append(inspect.getfile(func))
    except Exception:
        pass
    try:
        module_name = getattr(func, '__module__', '').split('.')[-1]
        if module_name:
            import os
            for base in (os.getcwd(), os.path.join(os.getcwd(), 'pages')):
                for ext in ('.py', '.psx'):
                    candidates.append(os.path.join(base, module_name + ext))
    except Exception:
        pass
    # Dynamically executed page modules often have no usable filename.  Scan
    # the pages tree for the component definition as a last resort.
    try:
        import os
        func_name = getattr(func, '__name__', '')
        pages_dir = os.path.join(os.getcwd(), 'pages')
        if func_name and os.path.isdir(pages_dir):
            for root, _dirs, files in os.walk(pages_dir):
                for filename in files:
                    if not filename.endswith(('.py', '.psx')):
                        continue
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except Exception:
                        continue
                    if f'def {func_name}(' in content:
                        candidates.insert(0, file_path)
                        break
                if candidates and candidates[0].startswith(pages_dir):
                    break
    except Exception:
        pass
    for file_path in candidates:
        try:
            if file_path and os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception:
            continue
    try:
        return inspect.getsource(func)
    except Exception:
        return ""


def _extract_state_and_derived(func: Callable) -> Tuple[List[str], Dict[str, str]]:
    """Extract useState keys and simple derived-variable expressions.

    Derived values such as ``bg_color = "bg-white" if theme == "light" else
    ...`` are evaluated by Python during SSR and then lost.  Capturing the
    expression lets the browser recompute the same value after a state change.
    """
    source = _get_component_source(func)
    state_keys: List[str] = []
    derived: Dict[str, str] = {}
    if not source:
        return state_keys, derived

    try:
        import textwrap
        tree = ast.parse(textwrap.dedent(source))
    except Exception:
        return state_keys, derived

    node = None
    for candidate in ast.walk(tree):
        if isinstance(candidate, (ast.FunctionDef, ast.AsyncFunctionDef)) and candidate.name == getattr(func, '__name__', ''):
            node = candidate
            break
    if node is None:
        return state_keys, derived

    hook_names = {
        'useState', 'useEffect', 'useFetch', 'useReducer', 'useMemo',
        'useCallback', 'useRef', 'useContext', 'useLocalStorage',
        'useDebounce', 'useInterval', 'useToggle', 'useCrudEvent',
    }
    excluded_names = {
        'handle', 'handler', 'props', 'result', 'children',
    }

    for stmt in node.body:
        if isinstance(stmt, ast.Assign):
            value = stmt.value
            targets = stmt.targets
            # [state, setter] = useState(...)
            if len(targets) == 1 and isinstance(targets[0], (ast.Tuple, ast.List)):
                if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == 'useState':
                    elts = targets[0].elts
                    if elts and isinstance(elts[0], ast.Name):
                        state_keys.append(elts[0].id)
                continue
            if len(targets) != 1 or not isinstance(targets[0], ast.Name):
                continue
            name = targets[0].id
            if name in excluded_names or name.startswith('_'):
                continue
            if isinstance(value, (ast.Lambda, ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
                if value.func.id in hook_names or value.func.id.startswith('create_on'):
                    continue
            try:
                expr = ast.unparse(value).strip()
            except Exception:
                continue
            if expr:
                derived[name] = expr
        elif isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

    return state_keys, derived


def _extract_client_effects(func: Callable) -> List[Dict[str, Any]]:
    """Compile useEffect callbacks into structured client actions."""
    source = _get_component_source(func)
    if not source:
        return []
    try:
        import textwrap
        tree = ast.parse(textwrap.dedent(source))
    except Exception:
        return []

    node = None
    for candidate in ast.walk(tree):
        if isinstance(candidate, (ast.FunctionDef, ast.AsyncFunctionDef)) and candidate.name == getattr(func, '__name__', ''):
            node = candidate
            break
    if node is None:
        return []

    defs = {
        child.name: child for child in node.body
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    from ..compiler.actions import compile_handler_to_actions
    effects: List[Dict[str, Any]] = []
    for stmt in node.body:
        if not (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call)):
            continue
        call = stmt.value
        if not (isinstance(call.func, ast.Name) and call.func.id == 'useEffect'):
            continue
        if not call.args:
            continue

        arg = call.args[0]
        code = None
        name = 'effect'
        if isinstance(arg, ast.Lambda):
            code = ast.unparse(arg)
            name = 'effect'
        elif isinstance(arg, ast.Name) and arg.id in defs:
            target = defs[arg.id]
            name = arg.id
            body = target.body
            # Drop nonlocal/global declarations; state writes become SET_STATE.
            body = [b for b in body if not isinstance(b, (ast.Nonlocal, ast.Global))]
            code = '\n'.join(ast.unparse(b) for b in body)
        if not code:
            continue

        deps = None
        if len(call.args) > 1:
            deps_node = call.args[1]
            if isinstance(deps_node, (ast.List, ast.Tuple)):
                try:
                    deps = [ast.literal_eval(elt) for elt in deps_node.elts]
                except Exception:
                    deps = [ast.unparse(elt) for elt in deps_node.elts]
        try:
            actions = compile_handler_to_actions(code, name)
        except Exception:
            actions = []
        if actions and not any(
            isinstance(a, dict) and (a.get('metadata') or {}).get('error')
            for a in actions
        ):
            effects.append({'name': name, 'actions': actions, 'deps': deps})

    return effects


def interactive_component(func: Callable) -> Callable:
    """
    Decorator for interactive PSX components with client-side state management.
    
    Properly handles named event handler functions and converts them to JavaScript.
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
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
            handlers = {}
        
        if not handlers:
            try:
                handlers = extract_handler_functions(func)
            except Exception as e:
                handlers = {}
        
        # Extract create_on handlers FIRST to get python_call_lambda_* placeholders
        try:
            create_handlers, _ = extract_create_handler_assignments(func, handlers)
            if create_handlers:
                handlers.update(create_handlers)
        except Exception as e:
            pass
        
        # Extract handlers using new AST-based compiler
        try:
            from ..compiler.handler_compiler import extract_handlers_compiled
            ast_handlers = extract_handlers_compiled(func, func.__name__)
            if ast_handlers:
                handlers.update(ast_handlers)
        except Exception as e:
            pass
        
        # FIX: Generate component ID early and pass to component execution
        from .engine import get_hydration_engine
        engine = get_hydration_engine()
        component_id = engine.generate_component_id()
        
        # FIX: Pass component_id directly to component function as a prop
        if props is None:
            props = {}
        props['_component_id'] = component_id
        
        # Execute through the base decorator so props, local helpers, and
        # module-level components are captured in ``_psx_context``. Calling
        # the raw ``func`` here loses nested functions used inside {for}/{if}
        # blocks (e.g. job_type_label) and breaks their evaluation.
        base_component_result = base_component(func)(props)

        # Snapshot mount actions before rendering children.  Child components
        # reset the thread-local hook state, so reading it after ``to_html``
        # would pick up a child's actions (or none) instead of this component's.
        from ..components.component import get_current_component
        _comp_state = get_current_component()
        _mount_actions_snapshot = list(getattr(_comp_state, 'mount_actions', []))
        _registered_functions_snapshot = dict(
            getattr(_comp_state, 'registered_functions', {})
        )
        
        # FIX: Extract state early before rendering
        from .integration import get_component_hydrator
        hydrator = get_component_hydrator()
        metadata = hydrator.extract_component_metadata(func)
        initial_state = metadata['state']
        state_keys, derived_expressions = _extract_state_and_derived(func)
        if not state_keys:
            state_keys = list(initial_state.keys())
        client_effects = _extract_client_effects(func)
        
        # Get the HTML output with interactive handler context
        if hasattr(base_component_result, 'to_html'):
            # Check if this is a PSX element with context
            if hasattr(base_component_result, '_psx_context'):
                # Add interactive handlers to the context for PSX runtime processing
                base_component_result._psx_context['_interactive_handlers'] = {name: True for name in handlers.keys()}
                # FIX: Add extracted state to the context for data binding
                base_component_result._psx_context.update(initial_state)
                # FIX: Add component ID to context for conditional element tracking
                base_component_result._psx_context['_component_id'] = component_id
                # Expose which values may change in the browser.  Attribute
                # rendering uses this to emit reactive class/style bindings
                # even when the component used an f-string (which Python has
                # already flattened before PSX sees it).
                base_component_result._psx_context['_psx_dynamic_vars'] = list(dict.fromkeys(
                    list(state_keys) + list(derived_expressions.keys())
                ))
                base_component_result._psx_context['_psx_derived_expressions'] = derived_expressions
                html = base_component_result.to_html()  # Don't pass context, use stored _psx_context
                
                # FIX: Post-process HTML to add component_id to conditional elements
                # This is a fallback mechanism to ensure conditional elements have the component_id
                def add_component_id_to_conditionals(html, component_id):
                    # Pattern to match conditional spans with empty component_id
                    # Handle both escaped and unescaped quotes
                    pattern = r'<span\s+data-component-id=""\s+data-if-condition="([^"]*)"'
                    replacement = f'<span data-component-id="{component_id}" data-if-condition="\\1"'
                    result = re.sub(pattern, replacement, html)
                    matches = re.findall(pattern, html)
                    if not matches:
                        # Try alternative pattern with different spacing
                        pattern2 = r'<span data-component-id="" data-if-condition="([^"]*)"'
                        matches2 = re.findall(pattern2, html)
                        result = re.sub(pattern2, replacement, html)
                    return result
                html = add_component_id_to_conditionals(html, component_id)
            else:
                html = base_component_result.to_html()
        else:
            html = str(base_component_result)
        
        # Supplement state keys from the rendered context.  inspect.getsource
        # often fails for dynamically loaded pages, but the context still has
        # the actual useState variable names (e.g. full_name, confirming_delete).
        if hasattr(base_component_result, '_psx_context'):
            for _key, _value in base_component_result._psx_context.items():
                if not callable(_value) and not str(_key).startswith('_') and _key not in state_keys:
                    state_keys.append(_key)

        # FIX: Extract lambda handlers from _psx_context (set by PSXRuntime during rendering)
        if hasattr(base_component_result, '_psx_context'):
            lambda_handlers = base_component_result._psx_context.get('_lambda_handlers', {})
            if lambda_handlers:
                from ..compiler.actions import compile_handler_to_actions
                for handler_name, lambda_source in lambda_handlers.items():
                    try:
                        actions = compile_handler_to_actions(lambda_source, handler_name)
                        if actions and not any(
                            isinstance(a, dict) and (a.get('metadata') or {}).get('error')
                            for a in actions
                        ):
                            handlers[handler_name] = actions
                        else:
                            handlers[handler_name] = python_code_to_js(lambda_source, state_keys)
                    except Exception as e:
                        handlers[handler_name] = python_code_to_js(lambda_source, state_keys)
        
        # Compile any remaining Python handler strings into structured actions.
        # The regex fallbacks below historically emitted raw Python (e.g. a
        # ternary) directly into the browser, which is a SyntaxError.  Structured
        # actions keep the client runtime safe and make conditionals/derived
        # expressions behave the same on both sides.
        try:
            from ..compiler.actions import compile_handler_to_actions
            for _handler_name, _handler_body in list(handlers.items()):
                if not isinstance(_handler_body, str) or not _handler_body.strip():
                    continue
                _code = _handler_body.strip()
                # Do not feed already-compiled JavaScript back into the Python
                # action compiler (e.g. ``this.stateManager.set(...)``).
                if any(_marker in _code for _marker in (
                    'this.stateManager', 'executeNextPyActions', 'console.',
                    'window.', 'document.', 'new Function(', '=>'
                )):
                    continue
                _candidate = _code
                if not _code.startswith(('lambda ', 'lambda:', 'def ')) and '\n' not in _code:
                    _candidate = f"lambda e: {_code}"
                try:
                    _actions = compile_handler_to_actions(_candidate, _handler_name)
                    if _actions and not any(
                        isinstance(a, dict) and (a.get('metadata') or {}).get('error')
                        for a in _actions
                    ):
                        handlers[_handler_name] = _actions
                except Exception:
                    pass
        except Exception:
            pass

        # Convert handler attributes to data-handler attributes with dynamic targeting
        html = convert_handler_attributes_in_html(html, handlers, state_keys, initial_state)
        
        # Manually register component to ensure consistent ID
        component_data = {
            'name': metadata['name'],
            'state': metadata['state'],
            'handlers': metadata['handlers'],
            'effects': metadata['effects'],
            'props': props or {},
            'mount_actions': _mount_actions_snapshot,
            'registered_functions': _registered_functions_snapshot,
            'derived_expressions': derived_expressions,
            'client_effects': client_effects,
        }
        # Override the generated ID with our consistent one
        original_id = engine.register_component(component_data)
        engine.contexts[component_id] = engine.contexts[original_id]
        del engine.contexts[original_id]
        
        # Wrap HTML with hydration data using consistent ID
        state = metadata['state']
        hydrated_html = engine.generate_html_wrapper(component_id, html, state)
        
        
        # Generate scripts
        # Only emit this component's hydration script. Generating all
        # contexts makes every component embed every earlier component,
        # producing quadratic page size and leaking scripts across routes.
        full_script = engine.generate_hydration_script(component_id)
        
        handler_script = generate_handler_registration_script(handlers, component_id, state_keys=state_keys, html=html)
        hydration_script = hydrator.generate_hydration_script(component_id)
        
        # Load JS action runtime script for executeNextPyActions
        try:
            from ..runtime.js_actions_runtime import JS_ACTION_RUNTIME_SCRIPT
            action_runtime_script = JS_ACTION_RUNTIME_SCRIPT
        except ImportError:
            action_runtime_script = ""
        
        # Combine all scripts in correct order
        # 1. JS action runtime script (defines executeNextPyActions)
        # 2. Full runtime script (defines NextPyRuntime)
        # 3. Hydration script (initializes components)
        # 4. Handler registration script (uses executeNextPyActions)
        complete_script = f"{action_runtime_script}\n\n{full_script}\n\n{hydration_script}\n\n{handler_script}"
        
        # The script is self-contained now; drop the server-side context so
        # repeated page renders do not accumulate every component ever seen.
        engine.cleanup_component(component_id)
        
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
