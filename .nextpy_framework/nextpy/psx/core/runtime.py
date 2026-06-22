"""
PSX Runtime - Unified runtime with production-grade security
Integrates AST nodes, safe evaluation, and logic execution
"""

import ast
import html
from typing import Any, Dict, List, Optional, Union
from .ast_nodes import (
    PSXNode, PSXNodeUnion, ExpressionNode, LogicNode, IfNode, ForNode, WhileNode, TryNode, PSXASTParser,
    ElementNode, TextNode, ComponentNode, FragmentNode
)
from .evaluator import SafeExpressionEngine


class PSXRuntimeError(Exception):
    """Runtime error with context information"""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.context = context or {}


class PSXRuntime:
    """Production-grade PSX runtime with AST integration"""
    
    def __init__(self, context: Dict[str, Any] = None):
        self.context = context or {}
        self.evaluator = SafeExpressionEngine(self.context)
        self.ast_parser = PSXASTParser()
        
        # Performance: Cache compiled expressions
        self._expression_cache: Dict[str, Any] = {}
        
        # Context stack for proper variable scoping in nested loops
        self._context_stack = [self.context] if context else [{}]
    
    def update_context(self, new_context: Dict[str, Any]):
        """Update the runtime context with new variables"""
        self.context.update(new_context)
        # Update evaluator context
        self.evaluator.context = self.context
        # Clear cache since context changed
        self._expression_cache.clear()
    
    def push_context(self, new_context: Dict[str, Any]):
        """Push a new context onto the stack for nested scoping"""
        self._context_stack.append(new_context)
        self.context = new_context
        self.evaluator.context = new_context
    
    def pop_context(self):
        """Pop the current context and restore the previous one"""
        if len(self._context_stack) > 1:
            self._context_stack.pop()
            self.context = self._context_stack[-1]
            self.evaluator.context = self.context
    
    def lookup_variable(self, var_name: str) -> Any:
        """Look up variable in the context stack (top-down)"""
        for ctx in reversed(self._context_stack):
            if var_name in ctx:
                return ctx[var_name]
        raise KeyError(f"Variable '{var_name}' not found in context")
    
    def evaluate_expression(self, expression: str) -> Any:
        """Safely evaluate an expression with caching"""
        # Check cache first
        if expression in self._expression_cache:
            return self._expression_cache[expression]
        
        try:
            result = self.evaluator.evaluate(expression)
            # Cache simple expressions
            if self._is_cacheable(expression):
                self._expression_cache[expression] = result
            return result
        except Exception as e:
            raise PSXRuntimeError(f"Expression evaluation failed: {expression}. Error: {e}")
    
    def evaluate_ast_expression(self, expression_node: ExpressionNode) -> Any:
        """Evaluate parsed AST expression node"""
        if expression_node.parsed_expression:
            return self.evaluator._evaluate_node(expression_node.parsed_expression)
        else:
            # Parse and cache if not already parsed
            parsed = self.ast_parser.parse_expression(expression_node.expression)
            expression_node.parsed_expression = parsed
            if parsed:
                return self.evaluator._evaluate_node(parsed)
            else:
                return self.evaluate_expression(expression_node.expression)
    
    def execute_logic(self, node: LogicNode) -> str:
        """Execute a logic block using AST structure"""
        try:
            if isinstance(node, IfNode):
                return self._execute_if(node)
            elif isinstance(node, ForNode):
                return self._execute_for(node)
            elif isinstance(node, WhileNode):
                return self._execute_while(node)
            elif isinstance(node, TryNode):
                return self._execute_try(node)
            else:
                return html.escape(f"[Unknown Logic Type: {node.logic_type}]")
        except Exception as e:
            return html.escape(f"[Logic Error: {e}]")
    
    def _execute_if(self, node: IfNode) -> str:
        """Execute if/elif/else logic block using AST"""
        # Evaluate condition
        if node.parsed_condition:
            condition_result = self.evaluator._evaluate_node(node.parsed_condition)
        else:
            condition_result = self.evaluate_expression(node.condition)
        
        # FIX: Render both branches for client-side conditional updates
        then_result = self._render_node_list(node.then_body)
        else_result = ""
        
        if condition_result:
            result = then_result
        else:
            # Check elif conditions
            for i, (elif_cond, elif_body) in enumerate(zip(node.elif_conditions, node.elif_bodies)):
                # Check parsed condition first
                if i < len(node.elif_parsed_conditions) and node.elif_parsed_conditions[i]:
                    elif_result = self.evaluator._evaluate_node(node.elif_parsed_conditions[i])
                else:
                    elif_result = self.evaluate_expression(elif_cond)
                
                if elif_result:
                    result = self._render_node_list(elif_body)
                    return result
            
            # Execute else if present
            if node.else_body:
                else_result = self._render_node_list(node.else_body)
                result = else_result
            else:
                result = ""
        
        # FIX: Wrap conditional content in a span with data attributes for client-side updates
        escaped_condition = html.escape(node.condition)
        escaped_then = html.escape(then_result)
        escaped_else = html.escape(else_result)
        
        return f'<span data-if-condition="{escaped_condition}" data-if-true="{escaped_then}" data-if-false="{escaped_else}">{result}</span>'
    
    def _execute_for(self, node: ForNode) -> str:
        """Execute for loop logic block using AST with proper variable scoping"""
        # Evaluate iterable
        if node.parsed_iterable:
            iterable = self.evaluator._evaluate_node(node.parsed_iterable)
        else:
            iterable = self.evaluate_expression(node.iterable)
        
        result_parts = []
        for item in iterable:
            # Create a new local context, keeping outer variables intact
            local_context = dict(self.context)  # copy outer context
            local_context[node.variable] = item

            # Push context onto stack for proper scoping
            self.push_context(local_context)
            
            try:
                # Render with the new context
                result_parts.append(self._render_node_list(node.body))
            finally:
                # Always pop context to maintain stack integrity
                self.pop_context()
        
        return "".join(result_parts)
    
    def _execute_while(self, node: WhileNode) -> str:
        """Execute while loop logic block using AST"""
        result_parts = []
        local_context = {**self.context}
        local_runtime = PSXRuntime(local_context)
        
        while True:
            # Evaluate condition
            if node.parsed_condition:
                condition_result = local_runtime.evaluator._evaluate_node(node.parsed_condition)
            else:
                condition_result = local_runtime.evaluate_expression(node.condition)
            
            if not condition_result:
                break
            
            result_parts.append(local_runtime._render_node_list(node.body))
        
        return "".join(result_parts)
    
    def _execute_try(self, node: TryNode) -> str:
        """Execute try/except/finally logic block"""
        try:
            # Execute try body
            result = self._render_node_list(node.try_body)
            return result
        except Exception as e:
            # Execute except if present
            if node.except_body:
                local_context = {**self.context}
                if node.except_var:
                    local_context[node.except_var] = e
                local_runtime = PSXRuntime(local_context)
                return local_runtime._render_node_list(node.except_body)
            else:
                return html.escape(f"[Exception: {e}]")
        finally:
            # Execute finally if present
            if node.finally_body:
                local_runtime = PSXRuntime(self.context)
                return local_runtime._render_node_list(node.finally_body)
    
    def _render_node_list(self, nodes: List[PSXNodeUnion]) -> str:
        """Render a list of AST nodes to HTML"""
        result_parts = []
        for node in nodes:
            result_parts.append(self._render_node(node))
        return "".join(result_parts)
    
    def _render_node(self, node: PSXNodeUnion) -> str:
        """Render a single AST node to HTML"""
        if isinstance(node, ExpressionNode):
            result = self.evaluate_ast_expression(node)
            # Check if result is a PSXElement
            if hasattr(result, 'to_html'):
                return result.to_html()
            else:
                # Check if this is a simple variable reference that should be bound
                expr = node.expression.strip()
                # Simple heuristic: if expression is a single variable name in context
                # wrap it in a span with data-bind attribute for reactive updates
                if expr in self.context and not any(c in expr for c in '+-*/%()[]{}'):
                    # This looks like a state variable, add binding
                    result_str = str(result)
                    return f'<span data-bind="textContent:{expr}">{html.escape(result_str)}</span>'
                else:
                    return html.escape(str(result))
        elif isinstance(node, LogicNode):
            return self.execute_logic(node)
        elif isinstance(node, ElementNode):
            return self._render_element_node(node)
        elif isinstance(node, TextNode):
            # Use proper HTML detection with regex
            import html
            import re
            
            HTML_TAG_RE = re.compile(r'</?[a-zA-Z][^>]*>')
            content = node.content
            
            # Check if content looks like HTML (has actual HTML tags)
            if HTML_TAG_RE.search(content):
                return content
            # Check if content starts with > but has more content (processed control flow output)
            elif content.startswith('>') and len(content) > 1:
                # Remove the leading > and return the rest as-is
                return content[1:]
            else:
                return html.escape(content)
        elif isinstance(node, ComponentNode):
            return self._render_component_node(node)
        elif isinstance(node, FragmentNode):
            return self._render_node_list(node.children)
        else:
            return str(node)
    
    def _render_element_node(self, node: 'ElementNode') -> str:
        """Render an ElementNode to HTML with proper JSX->HTML conversion"""
        # Convert JSX attributes to HTML attributes
        attrs = []
        for key, value in node.attributes.items():
            # Handle special bind attributes set by the parser
            if key == '_bind_target':
                # This is a special attribute set by the parser for bind directive
                # Convert to data-bind attribute for runtime handling
                bind_target = value
                bind_type = node.attributes.get('_bind_type', 'value')
                # Override bind_type for checkboxes regardless of attribute declaration order
                if node.tag == 'input' and node.attributes.get('type') == 'checkbox':
                    bind_type = 'checked'
                attrs.append(f'data-bind="{bind_type}:{bind_target}"')
                # Also set the initial value from the context
                if bind_target in self.context:
                    initial_value = self.context[bind_target]
                    if bind_type == 'value':
                        attrs.append(f'value="{html.escape(str(initial_value))}"')
                    elif bind_type == 'checked':
                        if initial_value:
                            attrs.append('checked')
                continue
            elif key == '_bind_type':
                # Skip this attribute, it's already handled above
                continue
            
            # JSX -> HTML attribute mapping
            if key == 'className':
                html_key = 'class'
            elif key == 'htmlFor':
                html_key = 'for'
            else:
                html_key = key

            # Convert style object into inline CSS text
            if html_key == 'style' and isinstance(value, dict):
                style_value = '; '.join(f'{k}: {v}' for k, v in value.items())
                value = style_value

            # Handle boolean and null-like attributes correctly
            if isinstance(value, bool):
                if value:
                    attrs.append(f'{html_key}')
                continue
            if value is None:
                continue

            # Handle different value types
            if isinstance(value, str):
                # Don't escape already HTML content
                if '<' in value and '>' in value:
                    attrs.append(f'{html_key}="{value}"')
                else:
                    attrs.append(f'{html_key}="{html.escape(value)}"')
            else:
                attrs.append(f'{html_key}="{html.escape(str(value))}"')
        
        # Handle events (onClick, onChange, etc.) with interactive component integration
        for key, value in node.events.items():
            # Keep event handlers as they are or wrap them if needed
            str_value = str(value)
            if str_value.startswith('{') and str_value.endswith('}'):
                str_value = str_value[1:-1]
            
            # Check if we should apply interactive component conversion
            if hasattr(self.context, '_interactive_handlers') and str_value in self.context._interactive_handlers:
                # This is an interactive component - convert to data-handler format
                event_type = key[2:].lower() if key.startswith('on') else key.lower()
                attrs.append(f'data-handler-{event_type}="{str_value}"')
                attrs.append(f'{key}="return false;"')
            else:
                # Regular event handler
                attrs.append(f'{key}="{self._escape_html(str_value)}"')
            
        attr_str = " " + " ".join(attrs) if attrs else ""
        
        if node.self_closing:
            # Ensure tag name is not empty
            tag = node.tag if node.tag else 'div'
            return f'<{tag}{attr_str} />'
            
        html_content = f'<{node.tag}{attr_str}>'
        html_content += self._render_node_list(node.children)
        html_content += f'</{node.tag}>'
        
        return html_content
    
    def _render_component_node(self, node: 'ComponentNode') -> str:
        """Render a ComponentNode to HTML with proper evaluation"""
        # Try to find the component in the context
        component_fn = self.context.get(node.name)
        
        # If not found in context, try the global component registry
        if not callable(component_fn):
            try:
                from ..components.component import component_registry
                component_fn = component_registry.get(node.name)
            except ImportError:
                pass
        
        if callable(component_fn):
            try:
                # Prepare props from node props (ComponentNode uses 'props' not 'attributes')
                props = dict(getattr(node, 'props', {}))
                
                # Add events to props
                for key, value in node.events.items():
                    props[key] = value
                
                # Add spread props to props
                for spread_prop in node.spread_props:
                    if spread_prop in self.context:
                        spread_data = self.context[spread_prop]
                        if isinstance(spread_data, dict):
                            props.update(spread_data)
                
                # Add children as a special prop if needed
                if node.children:
                    # Import PSXElement from the correct location
                    from .parser import PSXElement
                    
                    children_element = PSXElement(tag='fragment', props={}, children=node.children)
                    children_element._psx_context = self.context
                    props['children'] = children_element
                
                # Call the component function
                result = component_fn(**props)
                
                # Handle the result
                if hasattr(result, 'to_html'):
                    return result.to_html()
                elif hasattr(result, '_ast_node'):
                    # It's a PSXElement, render it
                    temp_runtime = PSXRuntime(self.context)
                    return temp_runtime._render_node(result._ast_node)
                else:
                    return str(result)
                    
            except Exception as e:
                # Fallback to error div
                return f'<div class="component-error">Error rendering {node.name}: {html.escape(str(e))}</div>'
        else:
            # Component not found, render as placeholder div
            return f'<div class="component-{node.name}" data-missing="true">{self._render_node_list(node.children)}</div>'
    
    def update_context(self, new_context: Dict[str, Any]):
        """Update runtime context and clear cache"""
        self.context.update(new_context)
        self.evaluator = SafeExpressionEngine(self.context)
        self._expression_cache.clear()
    
    def _is_cacheable(self, expression: str) -> bool:
        """Check if expression is safe to cache"""
        # Don't cache expressions that might change
        dangerous_keywords = ['random', 'time', 'datetime', 'now']
        return not any(keyword in expression.lower() for keyword in dangerous_keywords)
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters in text"""
        return html.escape(text)


def process_python_logic(psx_str: str, context: Dict[str, Any]) -> str:
    """
    Process Python logic in PSX strings
    Handles all Python expressions, PSX utilities, and control flow
    """
    import re
    import ast
    
    def is_safe_expression(expr: str) -> bool:
        """Check if expression is valid Python-like (not JSX/text)"""
        
        # Reject obvious HTML / JSX
        if '<' in expr or '>' in expr:
            return False
        
        # Reject plain text (contains spaces but no operators)
        # BUT allow valid variable names and simple expressions
        if ' ' in expr and not any(op in expr for op in ['+', '-', '*', '/', '==', '(', ')', '[', ']', '.', 'and', 'or', 'not', 'in', 'is']):
            return False
        
        # Reject malformed expressions
        if expr.count('(') != expr.count(')'):
            return False
        
        # Reject expressions that look like concatenated text
        if ' ' in expr and expr.replace(' ', '').isalpha():
            return False
        
        return True
    
    # Add PSX utilities to context
    enhanced_context = context.copy()
    
    # Add common Python builtins that are safe
    safe_builtins = {
        'len': len, 'str': str, 'int': int, 'float': float, 'bool': bool,
        'list': list, 'dict': dict, 'tuple': tuple, 'set': set,
        'range': range, 'enumerate': enumerate, 'zip': zip,
        'min': min, 'max': max, 'sum': sum, 'abs': abs,
        'round': round, 'sorted': sorted, 'reversed': reversed,
        'True': True, 'False': False, 'None': None,
    }
    enhanced_context.update(safe_builtins)
    
    # Add PSX utilities if not already present
    if 'clsx' not in enhanced_context:
        try:
            from ..components.component import clsx
            enhanced_context['clsx'] = clsx
        except:
            enhanced_context['clsx'] = lambda *args: ' '.join(str(arg) for arg in args if arg)
    
    def process_expression(expr_str: str) -> str:
        """Process a single Python expression"""
        try:
            # Create a safe evaluator with enhanced context
            engine = SafeExpressionEngine(enhanced_context)
            result = engine.evaluate(expr_str)
            
            # Handle different result types
            if isinstance(result, str):
                return result
            elif hasattr(result, '__iter__') and not isinstance(result, (str, bytes)):
                # Handle iterables (lists, etc.)
                if hasattr(result, 'map'):  # Check if it's a map object
                    return ''.join(str(item) for item in result)
                else:
                    return ''.join(str(item) for item in result)
            else:
                return str(result)
        except Exception as e:
            return f'{{Error: {expr_str} - {str(e)}}}'
    
    def process_control_flow(match):
        """Process control flow statements"""
        content = match.group(1).strip()
        
        # Handle for loops: {for item in items}...{/for}
        if content.startswith('for ') and ' in ' in content:
            try:
                # Parse for loop
                parts = content[3:].strip().split(' in ', 1)
                var_decl = parts[0].strip()
                iterable_expr = parts[1].strip().rstrip(':')
                
                # Find the loop body (content until {/for})
                full_match = match.group(0)
                start_pos = psx_str.find(full_match)
                end_pos = start_pos + len(full_match)
                
                # Find matching {/for}
                brace_count = 0
                for_pos = end_pos
                while for_pos < len(psx_str):
                    if psx_str[for_pos] == '{':
                        brace_count += 1
                    elif psx_str[for_pos] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            break
                    for_pos += 1
                
                # Extract loop body
                loop_body = psx_str[end_pos:for_pos]
                if loop_body.startswith('{/for}'):
                    loop_body = ''
                else:
                    # Remove {/for} at the end
                    loop_body = loop_body.replace('{/for}', '').strip()
                
                # Execute for loop
                engine = SafeExpressionEngine(enhanced_context)
                iterable = engine.evaluate(iterable_expr)
                
                result_parts = []
                for item in iterable:
                    # Set loop variable in context
                    if ' in ' in var_decl:
                        # Handle tuple unpacking: for key, value in items
                        var_names = [v.strip() for v in var_decl.split(' in ')[0].split(',')]
                        if isinstance(item, (list, tuple)) and len(item) == len(var_names):
                            for i, var_name in enumerate(var_names):
                                enhanced_context[var_name] = item[i]
                        else:
                            enhanced_context[var_names[0]] = item
                    else:
                        enhanced_context[var_decl] = item
                    
                    # Process loop body
                    processed_body = process_python_logic(loop_body, enhanced_context)
                    result_parts.append(processed_body)
                
                return ''.join(result_parts)
                
            except Exception as e:
                return f'{{For loop error: {str(e)}}}'
        
        # Handle if statements: {if condition}...{elif condition}...{else}...{/if}
        elif content.startswith('if '):
            try:
                condition = content[3:].strip()
                engine = SafeExpressionEngine(enhanced_context)
                
                # Find matching {/if}
                full_match = match.group(0)
                start_pos = psx_str.find(full_match)
                end_pos = start_pos + len(full_match)
                
                # Find matching {/if}
                brace_count = 0
                if_pos = end_pos
                while if_pos < len(psx_str):
                    if psx_str[if_pos] == '{':
                        brace_count += 1
                    elif psx_str[if_pos] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            break
                    if_pos += 1
                
                # Extract if body (until next control flow or {/if})
                if_body = psx_str[end_pos:if_pos]
                if_body = re.sub(r'\{/(if|elif|else)\}', '', if_body).strip()
                
                # Check for else clause
                else_body = ''
                if '{else:' in if_body:
                    if_part, else_part = if_body.split('{else:', 1)
                    if_body = if_part.strip()
                    else_body = else_part.strip()
                
                # Evaluate condition
                if engine.evaluate(condition):
                    result = process_python_logic(if_body, enhanced_context)
                else:
                    result = process_python_logic(else_body, enhanced_context) if else_body else ''
                
                # FIX: Wrap conditional content in a span with data attributes for client-side updates
                if_result = process_python_logic(if_body, enhanced_context)
                else_result = process_python_logic(else_body, enhanced_context) if else_body else ''
                
                # Escape the condition for HTML attribute
                escaped_condition = html.escape(condition)
                escaped_if_true = html.escape(if_result)
                escaped_if_false = html.escape(else_result)
                
                return f'<span data-if-condition="{escaped_condition}" data-if-true="{escaped_if_true}" data-if-false="{escaped_if_false}">{result}</span>'
                    
            except Exception as e:
                return f'{{If error: {str(e)}}}'
        
        # Handle elif and else (processed in if context)
        elif content.startswith('elif ') or content.startswith('else'):
            return ''  # These are handled by the if statement
        
        # Handle while loops: {while condition}...{/while}
        elif content.startswith('while '):
            try:
                condition = content[5:].strip()
                engine = SafeExpressionEngine(enhanced_context)
                
                # Find matching {/while}
                full_match = match.group(0)
                start_pos = psx_str.find(full_match)
                end_pos = start_pos + len(full_match)
                
                # Find matching {/while}
                brace_count = 0
                while_pos = end_pos
                while while_pos < len(psx_str):
                    if psx_str[while_pos] == '{':
                        brace_count += 1
                    elif psx_str[while_pos] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            break
                    while_pos += 1
                
                # Extract loop body
                loop_body = psx_str[end_pos:while_pos]
                loop_body = loop_body.replace('{/while}', '').strip()
                
                # Execute while loop (with safety limit)
                result_parts = []
                iterations = 0
                max_iterations = 1000  # Safety limit
                
                while engine.evaluate(condition) and iterations < max_iterations:
                    processed_body = process_python_logic(loop_body, enhanced_context)
                    result_parts.append(processed_body)
                    iterations += 1
                
                return ''.join(result_parts)
                
            except Exception as e:
                return f'{{While loop error: {str(e)}}}'
        
        # Handle try/except: {try}...{except}...{/try}
        elif content.startswith('try'):
            try:
                # Find matching {/try}
                full_match = match.group(0)
                start_pos = psx_str.find(full_match)
                end_pos = start_pos + len(full_match)
                
                # Find matching {/try}
                brace_count = 0
                try_pos = end_pos
                while try_pos < len(psx_str):
                    if psx_str[try_pos] == '{':
                        brace_count += 1
                    elif psx_str[try_pos] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            break
                    try_pos += 1
                
                # Extract try body
                try_body = psx_str[end_pos:try_pos]
                
                try:
                    return process_python_logic(try_body, enhanced_context)
                except Exception as e:
                    # Look for except block
                    except_match = re.search(r'\{except([^}]*)\}', psx_str[try_pos:])
                    if except_match:
                        except_body = psx_str[try_pos + len(except_match.group(0)):].split('{/try}')[0]
                        return process_python_logic(except_body, enhanced_context)
                    else:
                        return f'{{Error: {str(e)}}}'
                        
            except Exception as e:
                return f'{{Try block error: {str(e)}}}'
        
        # Handle function definitions (simplified)
        elif content.startswith('def '):
            return f'{{Function definitions not supported in PSX: {content}}}'
        
        # Handle class definitions (simplified)
        elif content.startswith('class '):
            return f'{{Class definitions not supported in PSX: {content}}}'
        
        # Handle import statements (simplified)
        elif content.startswith('import ') or content.startswith('from '):
            return f'{{Import statements not supported in PSX: {content}}}'
        
        return match.group(0)
    
    def process_control_flow_match(control_flow_block, enhanced_context):
        """Process a single control flow block"""
        # Remove outer braces
        content = control_flow_block[1:-1].strip()
        
        # Handle if statements: {if condition}...{else}...{/if}
        if content.startswith('if '):
            try:
                # Extract condition and body
                parts = content.split(':', 1)
                if len(parts) < 2:
                    return control_flow_block
                
                condition = parts[0][3:].strip()  # Remove 'if '
                body_content = parts[1]
                
                # Split into if and else parts
                if '{else:' in body_content:
                    if_part, else_part = body_content.split('{else:', 1)
                    if_part = if_part.rstrip('{/if').strip()
                    else_part = else_part.rstrip('{/if').strip()
                    
                    # Evaluate condition
                    engine = SafeExpressionEngine(enhanced_context)
                    if engine.evaluate(condition):
                        result = process_python_logic(if_part, enhanced_context)
                    else:
                        result = process_python_logic(else_part, enhanced_context)
                    
                    # FIX: Wrap conditional content in a span with data attributes for client-side updates
                    # This allows the JavaScript runtime to re-evaluate the condition when state changes
                    if_result = process_python_logic(if_part, enhanced_context)
                    else_result = process_python_logic(else_part, enhanced_context)
                    
                    # Escape the condition for HTML attribute
                    escaped_condition = html.escape(condition)
                    escaped_if_true = html.escape(if_result)
                    escaped_if_false = html.escape(else_result)
                    
                    return f'<span data-if-condition="{escaped_condition}" data-if-true="{escaped_if_true}" data-if-false="{escaped_if_false}">{result}</span>'
                else:
                    # Only if part
                    if_part = body_content.rstrip('{/if').strip()
                    engine = SafeExpressionEngine(enhanced_context)
                    if engine.evaluate(condition):
                        result = process_python_logic(if_part, enhanced_context)
                    else:
                        result = ''
                    
                    # FIX: Wrap conditional content in a span with data attributes for client-side updates
                    if_result = process_python_logic(if_part, enhanced_context)
                    escaped_condition = html.escape(condition)
                    escaped_if_true = html.escape(if_result)
                    
                    return f'<span data-if-condition="{escaped_condition}" data-if-true="{escaped_if_true}" data-if-false="">{result}</span>'
                        
            except Exception as e:
                return f'{{If error: {str(e)}}}'
        
        # Handle for loops: {for item in items}...{/for}
        elif content.startswith('for '):
            try:
                # Parse for loop: {for var in iterable:body{/for}
                if ':' not in content:
                    return control_flow_block
                
                # Split at the first colon to separate loop declaration from body
                parts = content.split(':', 1)
                loop_decl = parts[0][3:].strip()  # Remove 'for '
                loop_body = parts[1].rstrip('{/for}').strip()
                
                # Parse loop declaration: "var in iterable"
                if ' in ' not in loop_decl:
                    return control_flow_block
                
                var_parts = loop_decl.split(' in ', 1)
                var_name = var_parts[0].strip()
                iterable_expr = var_parts[1].strip().rstrip(':')
                
                # Execute for loop
                engine = SafeExpressionEngine(enhanced_context)
                iterable = engine.evaluate(iterable_expr)
                
                result_parts = []
                for item in iterable:
                    # Set loop variable in context
                    loop_context = enhanced_context.copy()
                    loop_context[var_name] = item
                    
                    # Process loop body (which may contain JSX)
                    processed_body = process_python_logic(loop_body, loop_context)
                    result_parts.append(processed_body)
                
                return ''.join(result_parts)
                
            except Exception as e:
                return f'{{For loop error: {str(e)}}}'
        
        return control_flow_block
    
    # Process control flow first (complex patterns)
    # Use a more sophisticated approach for control flow
    def process_control_flow_structures(text, enhanced_context):
        """Process control flow structures with proper brace matching"""
        result = []
        i = 0
        n = len(text)
        
        while i < n:
            if text[i] == '{':
                # Check if it's a control flow statement
                remaining = text[i+1:]
                if remaining.startswith('if ') or remaining.startswith('for ') or remaining.startswith('while '):
                    # Find the matching closing pattern like {/if}, {/for}, {/while}
                    if remaining.startswith('if '):
                        closing_pattern = '{/if}'
                    elif remaining.startswith('for '):
                        closing_pattern = '{/for}'
                    elif remaining.startswith('while '):
                        closing_pattern = '{/while}'
                    else:
                        closing_pattern = None
                    
                    if closing_pattern:
                        closing_pos = text.find(closing_pattern, i)
                        if closing_pos != -1:
                            # Include the closing pattern
                            control_flow_block = text[i:closing_pos + len(closing_pattern)]
                            # Process the control flow block
                            processed_block = process_control_flow_match(control_flow_block, enhanced_context)
                            result.append(processed_block)
                            i = closing_pos + len(closing_pattern)
                        else:
                            # No matching closing pattern, treat as text
                            result.append(text[i])
                            i += 1
                    else:
                        result.append(text[i])
                        i += 1
                else:
                    # Not a control flow statement, check if it's a simple expression
                    # Find the closing brace
                    closing_brace = text.find('}', i)
                    if closing_brace != -1:
                        # It's a simple expression, keep it as-is for now
                        # Our replace_all_expressions will handle it later
                        result.append(text[i:closing_brace + 1])
                        i = closing_brace + 1
                    else:
                        # No closing brace, treat as text
                        result.append(text[i])
                        i += 1
            else:
                result.append(text[i])
                i += 1
        
        # Clean up any leftover standalone braces
        result_text = ''.join(result)
        # Remove any remaining standalone } characters that aren't part of expressions
        # Only remove } that are not preceded by { (to avoid breaking expressions)
        result_text = result_text.replace('} ', ' ').replace('}\n', '\n').replace('}\r', '\r')
        
        return result_text
    
    # Use our unified expression processor that handles both control flow and simple expressions
    # Skip the separate control flow processing to avoid conflicts
    
    # Process everything in one unified pass
    result = psx_str
    
    # First pass: handle control flow structures
    # Look for complete control flow blocks and process them
    import re
        # Process if/else blocks - use simpler closing brace syntax
    def find_matching_if_block(text, start_pos):
        """Find a complete if/else block with simple closing brace"""
        start_brace = text.find('{if ', start_pos)
        if start_brace == -1:
            return None, -1
        
        # Find the end of the if condition (look for ':')
        end_condition = text.find(':', start_brace)
        if end_condition == -1:
            return None, -1
        
        # Extract the condition (between "if " and ":")
        condition = text[start_brace + 4:end_condition].strip()
        
        # Look for else block
        else_pos = text.find('{else:', end_condition)
        
        # Find the matching closing brace
        if else_pos != -1:
            # Has else block
            if_body = text[end_condition + 1:else_pos]
            
            # Find matching closing brace for the entire block
            # Start counting from after the else position
            brace_count = 1
            pos = else_pos + 6  # Skip '{else:'
            while pos < len(text) and brace_count > 0:
                if text[pos] == '{':
                    brace_count += 1
                elif text[pos] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = pos + 1
                        break
                pos += 1
            
            if brace_count == 0:
                else_body = text[else_pos + 6:end_pos - 1]  # Skip '{else:'
                return (condition, if_body, else_body, start_brace, end_pos)
        else:
            # No else block - find matching closing brace for if body
            brace_count = 1
            pos = end_condition + 1
            while pos < len(text) and brace_count > 0:
                if text[pos] == '{':
                    brace_count += 1
                elif text[pos] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = pos + 1
                        break
                pos += 1
            else:
                pos += 1
            
            if brace_count == 0:
                if_body = text[end_condition + 1:end_pos - 1]
                return (condition, if_body, None, start_brace, end_pos)
        
        return None, -1
    
    # Process for loops - use a simpler approach for basic for loops
    def find_matching_for_block(text, start_pos):
        """Find a complete for loop block with simple closing brace"""
        start_brace = text.find('{for ', start_pos)
        if start_brace == -1:
            return None, -1
        
        # Find the end of the for declaration (look for ':')
        end_decl = text.find(':', start_brace)
        if end_decl == -1:
            return None, -1
        
        # Extract the iterable expression (between "in" and ":")
        for_decl = text[start_brace:end_decl + 1]
        in_match = re.search(r'\{for\s+(\w+)\s+in\s+([^:}]+)', for_decl)
        if not in_match:
            return None, -1
        
        var_name = in_match.group(1)
        iterable_expr = in_match.group(2)
        
        # Find the matching closing brace for the entire for loop
        brace_count = 1
        pos = end_decl + 1
        while pos < len(text) and brace_count > 0:
            if text[pos] == '{':
                brace_count += 1
                pos += 1
            elif text[pos] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_pos = pos + 1
                    break
                pos += 1
            else:
                pos += 1
        
        if brace_count == 0:
            loop_body = text[end_decl + 1:end_pos - 1]
            return (var_name, iterable_expr, loop_body, start_brace, end_pos)
        else:
            return None, -1
    
    # Process all if/else blocks
    result = psx_str
    pos = 0
    while True:
        if_match = find_matching_if_block(result, pos)
        if not if_match or len(if_match) != 5:
            break
        
        condition, if_body, else_body, start_pos, end_pos = if_match
        
        try:
            engine = SafeExpressionEngine(enhanced_context)
            
            # FIX: Render both branches for client-side conditional updates
            if_result = process_python_logic(if_body, enhanced_context)
            else_result = process_python_logic(else_body, enhanced_context) if else_body else ''
            
            if engine.evaluate(condition):
                processed_content = if_result
            else:
                if else_body:
                    processed_content = else_result
                else:
                    processed_content = ''
            
            # FIX: Wrap conditional content in a span with data attributes for client-side updates
            escaped_condition = html.escape(condition)
            escaped_if_true = html.escape(if_result)
            escaped_if_false = html.escape(else_result)
            print('processed content', processed_content, escaped_condition, escaped_if_true, escaped_if_false)
            
            # FIX: Add data-component-id for dependency tracking
            component_id = enhanced_context.get('_component_id', '')
            print(f'DEBUG: enhanced_context keys: {list(enhanced_context.keys())}')
            print(f'DEBUG: Adding data-component-id="{component_id}" to conditional element')
            
            wrapped_content = f'<span data-if-condition="{escaped_condition}" data-if-true="{escaped_if_true}" data-if-false="{escaped_if_false}" data-component-id="{component_id}">{processed_content}</span>'
            
            # Replace the if/else block with the wrapped content
            result = result[:start_pos] + wrapped_content + result[end_pos:]
            pos = start_pos + len(wrapped_content)
            
        except:
            # If processing fails, skip this if block
            pos = end_pos
            continue
    
    # Process all for loops
    pos = 0
    while True:
        for_match = find_matching_for_block(result, pos)
        if not for_match or len(for_match) != 5:
            break
        
        var_name, iterable_expr, loop_body, start_pos, end_pos = for_match
        
        try:
            engine = SafeExpressionEngine(enhanced_context)
            iterable = engine.evaluate(iterable_expr)
            
            result_parts = []
            for item in iterable:
                # Create a new context for each iteration
                loop_context = enhanced_context.copy()
                loop_context[var_name] = item
                
                # Process the loop body with the new context
                processed_body = process_python_logic(loop_body, loop_context)
                result_parts.append(processed_body)
            
            # Replace the for loop with the processed content
            result = result[:start_pos] + ''.join(result_parts) + result[end_pos:]
            pos = start_pos + len(''.join(result_parts))
            
        except:
            # If processing fails, skip this for loop
            pos = end_pos
            continue
    
    # Now handle simple expressions with our improved logic
    matches = list(re.finditer(r'\{([^{}]+?)\}', result))
    if not matches:
        return result

    # Collect all replacements first
    replacements = []
    for match in matches:
        expr = match.group(1).strip()
        full_match = match.group(0)

        # Skip comments
        if expr.startswith('/*') and expr.endswith('*/'):
            replacements.append((full_match, ''))
            continue

        # Skip control flow (already processed)
        if any(expr.startswith(k) for k in [
            'for ', 'if ', 'while ', 'try', 'def ', 'class ',
            'import ', 'from ', 'elif ', 'else'
        ]):
            continue

        # 🚀 NEW: strict validation
        if not is_safe_expression(expr):
            continue

        try:
            engine = SafeExpressionEngine(enhanced_context)
            evaluated = engine.evaluate(expr)

            if isinstance(evaluated, str):
                replacement = evaluated
            elif hasattr(evaluated, 'to_html'):
                # PSX element / component result — skip text substitution here.
                # The AST renderer will call to_html() at the right time via _render_node.
                continue
            elif hasattr(evaluated, '__iter__') and not isinstance(evaluated, (str, bytes)):
                replacement = ''.join(str(x) for x in evaluated)
            else:
                replacement = str(evaluated)

            replacements.append((full_match, replacement))

        except Exception:
            # DO NOT break UI - just skip invalid expressions
            continue

    # Apply all replacements from end to start to avoid position conflicts
    for full_match, replacement in reversed(replacements):
        result = result.replace(full_match, replacement, 1)
    
    return result


# Global runtime instance
runtime = PSXRuntime()
