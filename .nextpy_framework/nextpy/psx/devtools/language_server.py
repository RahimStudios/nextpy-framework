"""
PSX Language Server - Real-time IntelliSense and Auto-completion
Provides VS Code-like language support for PSX with production-grade core integration
"""

import re
import json
import asyncio
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from ..core import PSXRuntime, PSXASTParser, PSXNodeValidator
from ..core.parser import PSXParser


@dataclass
class PSXCompletionItem:
    """PSX completion item for IntelliSense"""
    label: str
    kind: str  # 'method', 'function', 'variable', 'class', 'keyword'
    detail: str
    documentation: str
    insert_text: str
    filter_text: str
    sort_text: str


@dataclass
class PSXDiagnostic:
    """PSX diagnostic for error reporting"""
    range: Dict[str, int]  # {'start': line, 'end': line}
    severity: str  # 'error', 'warning', 'info', 'hint'
    message: str
    source: str = "PSX"


@dataclass
class PSXHover:
    """PSX hover information"""
    contents: str
    range: Dict[str, int]


@dataclass
class PSXSignatureHelp:
    """PSX signature help"""
    signatures: List[Dict[str, Any]]
    active_signature: int = 0
    active_parameter: int = 0


class PSXLanguageServer:
    """PSX Language Server for real-time IntelliSense with production-grade core"""
    
    def __init__(self):
        self.runtime = PSXRuntime()
        self.ast_parser = PSXASTParser()
        self.validator = PSXNodeValidator()
        self.parser = PSXParser()
        
        # PSX language definitions
        self.html_tags = [
            'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'button', 'input', 'form', 'img', 'a', 'ul', 'ol', 'li',
            'table', 'tr', 'td', 'th', 'section', 'article', 'header',
            'footer', 'nav', 'main', 'aside', 'select', 'option',
            'textarea', 'label', 'br', 'hr', 'strong', 'em', 'code',
            'pre', 'blockquote', 'figure', 'figcaption', 'iframe',
            'canvas', 'svg', 'path', 'circle', 'rect', 'polygon',
            'video', 'audio', 'source', 'track', 'details', 'summary',
            'dialog', 'menu', 'menuitem', 'progress', 'meter',
            'time', 'data', 'var', 'samp', 'kbd', 'sub', 'sup',
            'small', 'mark', 'b', 'i', 'u', 's', 'strike', 'del',
            'ins', 'ruby', 'rt', 'rp', 'bdi', 'bdo'
        ]
        
        self.events = [
            'onClick', 'onChange', 'onSubmit', 'onFocus', 'onBlur',
            'onKeyDown', 'onKeyUp', 'onKeyPress', 'onMouseDown',
            'onMouseUp', 'onMouseMove', 'onMouseEnter', 'onMouseLeave',
            'onMouseOver', 'onMouseOut', 'onDoubleClick', 'onWheel',
            'onTouchStart', 'onTouchEnd', 'onTouchMove', 'onTouchCancel',
            'onLoad', 'onUnload', 'onResize', 'onScroll', 'onError',
            'onAbort', 'onCanPlay', 'onCanPlayThrough', 'onDurationChange',
            'onEmptied', 'onEnded', 'onLoadedData', 'onLoadedMetadata',
            'onPause', 'onPlay', 'onPlaying', 'onProgress', 'onRateChange',
            'onSeeked', 'onSeeking', 'onStalled', 'onSuspend', 'onTimeUpdate',
            'onVolumeChange', 'onWaiting', 'onAnimationStart', 'onAnimationEnd',
            'onAnimationIteration', 'onTransitionEnd', 'onMessage', 'onOnline',
            'onOffline', 'onStorage', 'onHashChange', 'onPopState', 'onPageHide',
            'onPageShow', 'onBeforeUnload', 'onUnload', 'onResize', 'onScroll'
        ]
        
        self.attributes = [
            'class', 'className', 'id', 'style', 'title', 'alt', 'src',
            'href', 'target', 'rel', 'type', 'value', 'name', 'placeholder',
            'disabled', 'readOnly', 'required', 'checked', 'selected',
            'multiple', 'size', 'maxLength', 'minLength', 'pattern',
            'min', 'max', 'step', 'width', 'height', 'cols', 'rows',
            'wrap', 'accept', 'capture', 'autoComplete', 'autoFocus',
            'formAction', 'formEncType', 'formMethod', 'formNoValidate',
            'formTarget', 'inputMode', 'list', 'key'
        ]
        
        # Create completion items cache
        self.completion_cache = self._build_completion_cache()
    
    def _build_completion_cache(self) -> Dict[str, List[PSXCompletionItem]]:
        """Build completion items cache"""
        cache = {
            'html_tags': [],
            'events': [],
            'attributes': [],
            'utilities': [],
            'hooks': [],
            'components': []
        }
        
        # HTML tags
        for tag in self.html_tags:
            cache['html_tags'].append(PSXCompletionItem(
                label=tag,
                kind='class',
                detail=f'HTML {tag} element',
                documentation=f'<{tag}> - HTML element tag',
                insert_text=f'<{tag}>$1</{tag}>',
                filter_text=tag,
                sort_text=f'0{tag}'
            ))
        
        # Events
        for event in self.events:
            cache['events'].append(PSXCompletionItem(
                label=event,
                kind='method',
                detail=f'Event handler: {event}',
                documentation=f'{event} - Event handler for {event.replace("on", "").lower()} event',
                insert_text=f'{event}="$1"',
                filter_text=event,
                sort_text=f'1{event}'
            ))
        
        # Attributes
        for attr in self.attributes:
            cache['attributes'].append(PSXCompletionItem(
                label=attr,
                kind='property',
                detail=f'HTML attribute: {attr}',
                documentation=f'{attr} - HTML attribute',
                insert_text=f'{attr}="$1"',
                filter_text=attr,
                sort_text=f'2{attr}'
            ))
        
        # Utilities from language context
        utilities = {}  # Simplified for now
        for util_name, util_func in utilities.items():
            if callable(util_func) or isinstance(util_func, dict):
                cache['utilities'].append(PSXCompletionItem(
                    label=util_name,
                    kind='function',
                    detail=f'PSX utility: {util_name}',
                    documentation=self._get_utility_documentation(util_name),
                    insert_text=util_name,
                    filter_text=util_name,
                    sort_text=f'3{util_name}'
                ))
        
        # Add PSX hooks for auto-completion
        psx_hooks = {
            'useState': 'useState(initial) - React hook for state management',
            'useEffect': 'useEffect(callback, deps) - React hook for side effects',
            'useContext': 'useContext(context) - React hook for context consumption',
            'useReducer': 'useReducer(reducer, initial) - React hook for complex state',
            'useRef': 'useRef(initial) - React hook for mutable ref object',
            'useMemo': 'useMemo(callback, deps) - React hook for memoization',
            'useCallback': 'useCallback(callback, deps) - React hook for memoized callbacks',
            'useImperativeHandle': 'useImperativeHandle(ref, create) - React hook for imperative handles',
            'useLayoutEffect': 'useLayoutEffect(callback, deps) - React hook for layout effects',
            'useDebugValue': 'useDebugValue(value) - React hook for debugging values',
            'useTransition': 'useTransition() - React hook for state transitions',
            'useDeferredValue': 'useDeferredValue(value) - React hook for deferred values',
            'useId': 'useId() - React hook for unique IDs',
            # Custom hooks
            'useCounter': 'useCounter(initial) - Custom hook for counter state',
            'useToggle': 'useToggle(initial) - Custom hook for boolean toggle',
            'useLocalStorage': 'useLocalStorage(key, initial) - Custom hook for localStorage',
            'useFetch': 'useFetch(url) - Custom hook for API calls',
            'useDebounce': 'useDebounce(value, delay) - Custom hook for debounced values',
            'useInterval': 'useInterval(callback, delay) - Custom hook for intervals',
            'usePrevious': 'usePrevious(value) - Custom hook for previous value',
            'useAsync': 'useAsync(asyncFn, deps) - Custom hook for async operations',
            'useMediaQuery': 'useMediaQuery(query) - Custom hook for media queries',
            'useGeolocation': 'useGeolocation() - Custom hook for geolocation',
            'usePerformance': 'usePerformance() - Custom hook for performance metrics',
        }
        
        for hook_name, hook_doc in psx_hooks.items():
            cache['hooks'] = cache.get('hooks', [])
            cache['hooks'].append(PSXCompletionItem(
                label=hook_name,
                kind='function',
                detail=f'PSX Hook: {hook_name}',
                documentation=hook_doc,
                insert_text=f'{hook_name}($1)',
                filter_text=hook_name,
                sort_text=f'4{hook_name}'
            ))
        
        # Add PSX components and utilities
        psx_components = {
            'component': '@component - Decorator for PSX components',
            'psx': 'psx - PSX element creator',
            'render_psx': 'render_psx(element) - Render PSX element',
            'fragment': 'fragment - Fragment component',
            'key': 'key - Key prop for lists',
            'clsx': 'clsx(...classes) - Conditional class names',
            'VNode': 'VNode - Virtual DOM node',
            'create_element': 'create_element(type, props) - Create VDOM element',
            'process_python_logic': 'process_python_logic(code) - Process Python expressions',
            'runtime': 'runtime - PSX runtime instance',
            'compile_psx': 'compile_psx(file) - Compile PSX file',
            'PSXCompiler': 'PSXCompiler - PSX compilation utility',
        }
        
        for comp_name, comp_doc in psx_components.items():
            cache['components'] = cache.get('components', [])
            cache['components'].append(PSXCompletionItem(
                label=comp_name,
                kind='class' if comp_name[0].isupper() else 'function',
                detail=f'PSX {comp_name}',
                documentation=comp_doc,
                insert_text=comp_name,
                filter_text=comp_name,
                sort_text=f'5{comp_name}'
            ))
        
        # Add event handlers
        event_handlers = {
            'create_onclick': 'create_onclick(handler) - Click event handler',
            'create_onchange': 'create_onchange(handler) - Change event handler',
            'create_onsubmit': 'create_onsubmit(handler) - Submit event handler',
            'create_oninput': 'create_oninput(handler) - Input event handler',
            'create_onfocus': 'create_onfocus(handler) - Focus event handler',
            'create_onblur': 'create_onblur(handler) - Blur event handler',
            'create_onkeydown': 'create_onkeydown(handler) - Key down event handler',
            'create_onkeyup': 'create_onkeyup(handler) - Key up event handler',
            'create_onload': 'create_onload(handler) - Load event handler',
            'create_onresize': 'create_onresize(handler) - Resize event handler',
            'create_onscroll': 'create_onscroll(handler) - Scroll event handler',
        }
        
        for event_name, event_doc in event_handlers.items():
            cache['events'].append(PSXCompletionItem(
                label=event_name,
                kind='function',
                detail=f'Event Handler: {event_name}',
                documentation=event_doc,
                insert_text=f'{event_name}($1)',
                filter_text=event_name,
                sort_text=f'6{event_name}'
            ))
        
        return cache
    
    def _get_utility_documentation(self, util_name: str) -> str:
        """Get documentation for a utility"""
        docs = {
            'map': 'map(array, function) - Create a new array by applying function to each element',
            'filter': 'filter(array, function) - Create a new array with elements that pass the test',
            'reduce': 'reduce(array, function, initial) - Reduce array to a single value',
            'find': 'find(array, function) - Find first element that satisfies the test',
            'some': 'some(array, function) - Test if at least one element passes the test',
            'every': 'every(array, function) - Test if all elements pass the test',
            'forEach': 'forEach(array, function) - Execute function for each element',
            'length': 'length(array) - Get array length',
            'includes': 'includes(array, item) - Check if array contains item',
            'join': 'join(array, separator) - Join array elements into string',
            'slice': 'slice(array, start, end) - Extract portion of array',
            'push': 'push(array, item) - Add item to end of array',
            'pop': 'pop(array) - Remove and return last element',
            'toUpperCase': 'toUpperCase(string) - Convert string to uppercase',
            'toLowerCase': 'toLowerCase(string) - Convert string to lowercase',
            'trim': 'trim(string) - Remove whitespace from both ends',
            'split': 'split(string, separator) - Split string into array',
            'replace': 'replace(string, old, new) - Replace occurrences in string',
            'indexOf': 'indexOf(string, search) - Find index of substring',
            'startsWith': 'startsWith(string, prefix) - Check if string starts with prefix',
            'endsWith': 'endsWith(string, suffix) - Check if string ends with suffix',
            'Math': 'Math - Mathematical constants and functions',
            'console': 'console - Console logging utilities',
            'JSON': 'JSON - JSON parsing and stringification',
            'Date': 'Date - Date and time utilities',
            'clsx': 'clsx(...classes) - Conditional class names utility',
            'typeof': 'typeof(value) - Get type of value',
            'isArray': 'isArray(value) - Check if value is array',
            'isObject': 'isObject(value) - Check if value is object',
            'isString': 'isString(value) - Check if value is string',
            'isNumber': 'isNumber(value) - Check if value is number',
            'isFunction': 'isFunction(value) - Check if value is function',
            'ternary': 'ternary(condition, true, false) - Conditional expression',
            'and': 'and(a, b) - Logical AND',
            'or': 'or(a, b) - Logical OR',
            'not': 'not(value) - Logical NOT',
            'alert': 'alert(message) - Show alert message',
            'confirm': 'confirm(message) - Show confirmation dialog',
            'prompt': 'prompt(message, default) - Show input prompt',
            'setTimeout': 'setTimeout(callback, delay) - Execute callback after delay',
            'setInterval': 'setInterval(callback, interval) - Execute callback repeatedly',
        }
        
        return docs.get(util_name, f'{util_name} - PSX utility function')
    
    async def get_completions(self, text: str, position: int) -> List[PSXCompletionItem]:
        """Get completion items for position in text"""
        # Extract context around position
        start = max(0, position - 100)
        end = min(len(text), position + 100)
        context = text[start:end]
        
        # Determine what kind of completions to provide
        completions = []
        
        # Check if we're inside a tag
        if self._is_inside_tag(context, position - start):
            completions.extend(self.completion_cache['html_tags'])
        
        # Check if we're inside attributes
        if self._is_inside_attributes(context, position - start):
            completions.extend(self.completion_cache['attributes'])
            completions.extend(self.completion_cache['events'])
        
        # Check if we're inside an expression
        if self._is_inside_expression(context, position - start):
            completions.extend(self.completion_cache['utilities'])
            completions.extend(self.completion_cache['hooks'])
            completions.extend(self.completion_cache['components'])
            completions.extend(self.completion_cache['events'])
        
        # Always provide hooks and components at top level
        if self._is_at_top_level(context, position - start):
            completions.extend(self.completion_cache['hooks'])
            completions.extend(self.completion_cache['components'])
            completions.extend(self.completion_cache['events'])
        
        # Filter completions based on current word
        current_word = self._get_current_word(context, position - start)
        if current_word:
            completions = [c for c in completions if current_word.lower() in c.label.lower()]
        
        return completions
    
    def _is_inside_tag(self, context: str, pos: int) -> bool:
        """Check if position is inside a tag name"""
        before = context[:pos]
        after = context[pos:]
        
        # Look for < followed by tag name
        if re.search(r'<\s*[a-zA-Z]*$', before):
            return True
        
        return False
    
    def _is_inside_attributes(self, context: str, pos: int) -> bool:
        """Check if position is inside attributes"""
        before = context[:pos]
        
        # Look for tag name followed by attributes
        if re.search(r'<[a-zA-Z][^>]*\s+[a-zA-Z]*$', before):
            return True
        
        return False
    
    def _is_inside_expression(self, context: str, pos: int) -> bool:
        """Check if position is inside an expression"""
        before = context[:pos]
        
        # Count braces to see if we're inside {}
        open_braces = before.count('{')
        close_braces = before.count('}')
        
        return open_braces > close_braces
    
    def _get_current_word(self, context: str, pos: int) -> str:
        """Get current word at position"""
        before = context[:pos]
        
        # Find word characters before position
        match = re.search(r'([a-zA-Z_][a-zA-Z0-9_]*)$', before)
        if match:
            return match.group(1)
        
        return ''
    
    def _is_at_top_level(self, context: str, pos: int) -> bool:
        """Check if position is at top level (not inside tags or expressions)"""
        before = context[:pos]
        
        # Count braces and tags to determine context
        open_braces = before.count('{')
        close_braces = before.count('}')
        open_tags = before.count('<')
        close_tags = before.count('>')
        
        # At top level if not inside expressions or tags
        return (open_braces == close_braces and 
                not self._is_inside_attributes(before, len(before)) and
                not re.search(r'<\s*[a-zA-Z]*[^>]*$', before))
    
    async def get_diagnostics(self, text: str) -> List[PSXDiagnostic]:
        """Get diagnostic information for text using production-grade validator"""
        diagnostics = []
        
        try:
            # Parse PSX using production-grade parser
            ast_node = self.parser.parse_psx(text)
            
            # Validate using production-grade validator
            errors = self.validator.validate_node(ast_node)
            
            for error in errors:
                # Try to extract line information
                lines = text.split('\n')
                error_line = self._find_error_line(error, text)
                
                diagnostics.append(PSXDiagnostic(
                    range={'start': error_line, 'end': error_line + 1},
                    severity='error',
                    message=error,
                    source='PSX'
                ))
        
        except Exception as e:
            # Add parsing error
            diagnostics.append(PSXDiagnostic(
                range={'start': 0, 'end': 1},
                severity='error',
                message=f"PSX parsing error: {e}",
                source='PSX'
            ))
        
        return diagnostics
    
    def _find_error_line(self, error: str, text: str) -> int:
        """Find line number for error"""
        if 'position' in error:
            # Extract position from error message
            match = re.search(r'position (\d+)', error)
            if match:
                pos = int(match.group(1))
                return text[:pos].count('\n')
        
        return 0
    
    def _find_warning_line(self, warning: str, text: str) -> int:
        """Find line number for warning"""
        # Simple heuristic - return middle of document for now
        return text.split('\n') // 2
    
    async def get_hover(self, text: str, position: int) -> Optional[PSXHover]:
        """Get hover information for position"""
        # Get current word
        start = max(0, position - 50)
        context = text[start:position + 50]
        current_word = self._get_current_word(context, position - start)
        
        if not current_word:
            return None
        
        # Find documentation
        documentation = self.auto_complete.get_documentation(current_word)
        
        return PSXHover(
            contents=documentation,
            range={'start': position - len(current_word), 'end': position}
        )
    
    async def get_signature_help(self, text: str, position: int) -> Optional[PSXSignatureHelp]:
        """Get signature help for position"""
        # Check if we're inside a function call
        start = max(0, position - 100)
        context = text[start:position + 50]
        
        # Look for function calls
        match = re.search(r'([a-zA-Z_][a-zA-Z0-9_]*)\(', context)
        if match:
            func_name = match.group(1)
            
            # Get signature information
            signature = self._get_function_signature(func_name)
            if signature:
                return PSXSignatureHelp(
                    signatures=[signature],
                    active_signature=0,
                    active_parameter=0
                )
        
        return None
    
    def _get_function_signature(self, func_name: str) -> Optional[Dict[str, Any]]:
        """Get signature information for function"""
        signatures = {
            'map': {
                'label': 'map(array, function)',
                'documentation': 'Create a new array by applying function to each element',
                'parameters': [
                    {'label': 'array', 'documentation': 'Array to map over'},
                    {'label': 'function', 'documentation': 'Function to apply to each element'}
                ]
            },
            'filter': {
                'label': 'filter(array, function)',
                'documentation': 'Create a new array with elements that pass the test',
                'parameters': [
                    {'label': 'array', 'documentation': 'Array to filter'},
                    {'label': 'function', 'documentation': 'Test function'}
                ]
            },
            'reduce': {
                'label': 'reduce(array, function, initial)',
                'documentation': 'Reduce array to a single value',
                'parameters': [
                    {'label': 'array', 'documentation': 'Array to reduce'},
                    {'label': 'function', 'documentation': 'Reducer function'},
                    {'label': 'initial', 'documentation': 'Initial value'}
                ]
            },
            'clsx': {
                'label': 'clsx(...classes)',
                'documentation': 'Conditional class names utility',
                'parameters': [
                    {'label': 'classes', 'documentation': 'Class names or conditions'}
                ]
            },
            'useState': {
                'label': 'useState(initialValue)',
                'documentation': 'React state hook',
                'parameters': [
                    {'label': 'initialValue', 'documentation': 'Initial state value'}
                ]
            },
            'useEffect': {
                'label': 'useEffect(callback, dependencies)',
                'documentation': 'React effect hook',
                'parameters': [
                    {'label': 'callback', 'documentation': 'Effect callback function'},
                    {'label': 'dependencies', 'documentation': 'Dependency array'}
                ]
            }
        }
        
        return signatures.get(func_name)
    
    async def get_document_symbols(self, text: str) -> List[Dict[str, Any]]:
        """Get document symbols for navigation"""
        symbols = []
        
        # Find HTML tags
        for match in re.finditer(r'<([a-zA-Z][a-zA-Z0-9]*)', text):
            tag_name = match.group(1)
            line = text[:match.start()].count('\n')
            
            symbols.append({
                'name': tag_name,
                'kind': 'class',
                'location': {
                    'range': {
                        'start': {'line': line, 'character': match.start() - text.rfind('\n', 0, match.start()) - 1},
                        'end': {'line': line, 'character': match.end() - text.rfind('\n', 0, match.start()) - 1}
                    }
                }
            })
        
        return symbols
    
    async def get_code_actions(self, text: str, position: int) -> List[Dict[str, Any]]:
        """Get code actions for position"""
        actions = []
        
        # Get context
        start = max(0, position - 100)
        context = text[start:position + 50]
        
        # Suggest adding clsx for conditional classes
        if 'class=' in context and 'clsx(' not in text:
            actions.append({
                'title': 'Use clsx for conditional classes',
                'kind': 'quickfix',
                'edit': {
                    'changes': {
                        'file.py': [{
                            'range': {'start': position, 'end': position},
                            'newText': 'clsx('
                        }]
                    }
                }
            })
        
        # Suggest adding key to map items
        if '.map(' in context and 'key=' not in text:
            actions.append({
                'title': 'Add key prop to map items',
                'kind': 'quickfix',
                'edit': {
                    'changes': {
                        'file.py': [{
                            'range': {'start': position, 'end': position},
                            'newText': 'key={item.id}'
                        }]
                    }
                }
            })
        
        return actions


# Global language server instance
psx_language_server = PSXLanguageServer()


async def get_psx_completions(text: str, position: int) -> List[Dict[str, Any]]:
    """Get PSX completions - NO IMPORTS NEEDED!"""
    completions = await psx_language_server.get_completions(text, position)
    return [asdict(comp) for comp in completions]


async def get_psx_diagnostics(text: str) -> List[Dict[str, Any]]:
    """Get PSX diagnostics - NO IMPORTS NEEDED!"""
    diagnostics = await psx_language_server.get_diagnostics(text)
    return [asdict(diag) for diag in diagnostics]


async def get_psx_hover(text: str, position: int) -> Optional[Dict[str, Any]]:
    """Get PSX hover information - NO IMPORTS NEEDED!"""
    hover = await psx_language_server.get_hover(text, position)
    return asdict(hover) if hover else None


async def get_psx_signature_help(text: str, position: int) -> Optional[Dict[str, Any]]:
    """Get PSX signature help - NO IMPORTS NEEDED!"""
    signature_help = await psx_language_server.get_signature_help(text, position)
    return asdict(signature_help) if signature_help else None


async def get_psx_symbols(text: str) -> List[Dict[str, Any]]:
    """Get PSX document symbols - NO IMPORTS NEEDED!"""
    symbols = await psx_language_server.get_document_symbols(text)
    return symbols


async def get_psx_code_actions(text: str, position: int) -> List[Dict[str, Any]]:
    """Get PSX code actions - NO IMPORTS NEEDED!"""
    actions = await psx_language_server.get_code_actions(text, position)
    return actions


# Export all language server features
__all__ = [
    'PSXLanguageServer', 'PSXCompletionItem', 'PSXDiagnostic', 
    'PSXHover', 'PSXSignatureHelp',
    'get_psx_completions', 'get_psx_diagnostics', 'get_psx_hover',
    'get_psx_signature_help', 'get_psx_symbols', 'get_psx_code_actions',
    'psx_language_server'
]
