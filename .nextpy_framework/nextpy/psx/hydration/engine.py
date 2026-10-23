"""
NextPy Hydration Engine - Client-side Runtime for Interactive PSX Components
Clean, production-ready version with proper architecture
"""

import json
import re
import html
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class HydrationContext:
    """Context for a component being hydrated"""
    component_id: str
    component_name: str
    initial_state: Dict[str, Any] = field(default_factory=dict)
    event_handlers: Dict[str, str] = field(default_factory=dict)  # {eventName: pythonCode}
    use_effects: List[Dict[str, Any]] = field(default_factory=list)
    data_bindings: Dict[str, str] = field(default_factory=dict)  # {elementId: {prop: binding}}
    mount_actions: List[Dict[str, Any]] = field(default_factory=list)
    registered_functions: Dict[str, Any] = field(default_factory=dict)
    derived_expressions: Dict[str, str] = field(default_factory=dict)
    client_effects: List[Dict[str, Any]] = field(default_factory=list)


class HydrationEngine:
    """Main hydration engine for PSX components"""
    
    def __init__(self):
        self.component_counter = 0
        self.contexts: Dict[str, HydrationContext] = {}
        
    def generate_component_id(self) -> str:
        """Generate unique component ID"""
        self.component_counter += 1
        return f"psx_component_{self.component_counter}"
    
    def register_component(self, component_data: Dict[str, Any]) -> str:
        """Register a component for hydration"""
        component_id = self.generate_component_id()
        
        # SSR props must be available to client-side conditionals and
        # expressions (``user``, ``jobs``, ...). Only copy JSON-safe values so
        # request objects and other server-only state never reach the client.
        initial_state = dict(component_data.get('state') or {})
        for key, value in (component_data.get('props') or {}).items():
            if key.startswith('_') or key in initial_state:
                continue
            try:
                json.dumps(value)
            except (TypeError, ValueError):
                continue
            initial_state[key] = value
        
        context = HydrationContext(
            component_id=component_id,
            component_name=component_data.get('name', 'Component'),
            initial_state=initial_state,
            event_handlers=component_data.get('handlers', {}),
            use_effects=component_data.get('effects', []),
            mount_actions=component_data.get('mount_actions', []),
            registered_functions=component_data.get('registered_functions', {}),
            derived_expressions=component_data.get('derived_expressions', {}),
            client_effects=component_data.get('client_effects', []),
        )
        
        self.contexts[component_id] = context
        return component_id
    
    def generate_hydration_script(self, component_id: Optional[str] = None) -> str:
        """Generate JavaScript hydration script for a component or all components"""
        if component_id:
            # Generate script for specific component
            if component_id not in self.contexts:
                return ""
            
            context = self.contexts[component_id]
            
            return f"""
(function() {{
    'use strict';

    // Shared conservative HTML sanitizer for client-side innerHTML updates.
    if (!window.nextpySanitizeHTML) {{
        window.nextpySanitizeHTML = function(html) {{
            const template = document.createElement('template');
            template.innerHTML = String(html == null ? '' : html);
            const blocked = 'script,iframe,object,embed,link,meta,base,svg,math';
            template.content.querySelectorAll(blocked).forEach(node => node.remove());
            const walker = document.createTreeWalker(
                template.content, NodeFilter.SHOW_ELEMENT, null
            );
            const nodes = [];
            while (walker.nextNode()) nodes.push(walker.currentNode);
            nodes.forEach(node => {{
                Array.from(node.attributes).forEach(attr => {{
                    const name = attr.name.toLowerCase();
                    const value = String(attr.value || '').trim().toLowerCase();
                    const dangerousUrl = /^(javascript|vbscript|data:text\\/html|data:image\\/svg\\+xml):/.test(value);
                    if (name.startsWith('on') || name === 'srcdoc' ||
                        ((name === 'href' || name === 'src' || name === 'xlink:href' ||
                          name === 'formaction' || name === 'action') && dangerousUrl)) {{
                        node.removeAttribute(attr.name);
                    }}
                }});
            }});
            return template.innerHTML;
        }};
    }}

    // Component: {context.component_name}
    const componentId = '{component_id}';
    
    // Wait for DOM to be ready
    function initializeComponent() {{
        const element = document.getElementById(componentId);
        if (!element) {{
            console.warn('Component element not found:', componentId);
            return;
        }}
        
        // State manager
        class StateManager {{
        constructor(initialState) {{
            this.state = {{ ...initialState }};
            this.subscribers = [];
        }}
        
        get(key) {{
            return this.state[key];
        }}
        
        set(key, value) {{
            // Accept camelCase aliases from lambda setters even when useState
            // declared a snake_case variable (setFullName -> full_name).
            if (!(key in this.state)) {{
                const normalized = String(key).replace(/_/g, '').toLowerCase();
                const match = Object.keys(this.state).find(
                    (candidate) => candidate.replace(/_/g, '').toLowerCase() === normalized
                );
                if (match) key = match;
            }}
            const oldValue = this.state[key];
            this.state[key] = value;

            // Keep the action runtime's state in sync with DOM input bindings.
            // Input lambdas update StateManager directly, while server-action
            // params are evaluated from NextPyActionRuntime state.
            try {{
                const runtime = window.NextPyActionRuntime;
                const actionComponent = runtime && runtime.components && this.component && runtime.components.get(this.component.id);
                if (actionComponent) {{
                    actionComponent.state[key] = value;
                    // Re-evaluate conditionals, attribute bindings and derived
                    // expressions through the shared action runtime.  Without
                    // this bridge legacy ``create_on*`` handlers updated only
                    // ``data-bind`` text while ``data-if-condition`` blocks
                    // stayed frozen at their SSR state.
                    if (typeof runtime._triggerComponentUpdate === 'function' && !runtime._hydrationSyncDepth) {{
                        runtime._triggerComponentUpdate(this.component.id, key, value, oldValue);
                    }}
                }}
            }} catch (error) {{}}
            
            // CRITICAL: ONLY ONE UPDATE PATH - notify subscribers which triggers updateBindings
            this.notifySubscribers(key, value, oldValue);
        }}

        
        subscribe(callback) {{
            this.subscribers.push(callback);
            return () => {{
                const index = this.subscribers.indexOf(callback);
                if (index > -1) {{
                    this.subscribers.splice(index, 1);
                }}
            }};
        }}
        
        notifySubscribers(key, newValue, oldValue) {{
            // Notify all subscribers of state change
            this.subscribers.forEach(callback => {{
                try {{
                    callback(key, newValue, oldValue);
                }} catch (error) {{
                    console.error('State subscriber error:', error);
                }}
            }});
            
            // CRITICAL: Auto-trigger component binding updates after state changes
            if (this.component && this.component.updateBindings) {{
                this.component.updateBindings();
            }}
        }}
    }}
    
    // Component class
    class Component {{
        constructor(id, initialState) {{
            this.id = id;
            this.element = document.getElementById(id);
            this.stateManager = new StateManager(initialState);
            this.stateManager.component = this;  // CRITICAL: Set component reference
            this.unsubscribers = [];
            this.bindings = new Map();
            this.bindingCounter = 0;  // Counter for generating unique binding IDs
            
            if (!this.element) {{
                console.error('Component element not found:', id);
                return;
            }}
            
            this.setupDataBindings();
            this.setupEventHandlers();
            this.setupEffects();
            
            // Register with global action runtime so _executeVariable resolves state
            if (window.NextPyActionRuntime) {{
                window.NextPyActionRuntime.registerComponent(id, {{ ...initialState }});
                const _derivedExpressions = {json.dumps(context.derived_expressions)};
                const _runtimeComponent = window.NextPyActionRuntime.components.get(id);
                if (_runtimeComponent) {{
                    _runtimeComponent.derivedExpressions = _derivedExpressions;
                    _runtimeComponent.effects = {json.dumps(context.client_effects)};
                }}
                // FIX: Rebuild dependency map after DOM is ready
                setTimeout(() => {{
                    window.NextPyActionRuntime.rebuildDependencyMap(id);
                }}, 100);
            }}
        }}
        
        setupDataBindings() {{
            if (!this.element) return;
            
            const elements = this.element.querySelectorAll("[data-bind]");
            elements.forEach(element => {{
                const binding = element.getAttribute("data-bind");
                if (binding) {{
                    this.createBinding(element, binding);
                }}
            }});
        }}
        
        createBinding(element, binding) {{
            const parts = binding.split(":");
            if (parts.length !== 2) return;
            
            const [property, stateKey] = parts;
            const elementId = element.id || element.getAttribute('data-element-id') || `binding_${{this.bindingCounter++}}`;
            
            // Store binding info
            this.bindings.set(elementId, {{ property, stateKey, element }});
            
            // Subscribe to state changes
            const unsub = this.stateManager.subscribe((key, newValue) => {{
                if (key === stateKey) {{
                    this.updateBinding(elementId, property, newValue);
                }}
            }});
            
            this.unsubscribers.push(unsub);
            
            // Set initial value
            const initialValue = this.stateManager.get(stateKey);
            this.updateBinding(elementId, property, initialValue);
            
            // Add two-way binding for input elements
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA' || element.tagName === 'SELECT') {{
                element.addEventListener('input', (e) => {{
                    this.stateManager.set(stateKey, e.target.value);
                }});
                element.addEventListener('change', (e) => {{
                    this.stateManager.set(stateKey, e.target.value);
                }});
            }}
        }}
        
        updateBinding(elementId, property, value) {{
            const binding = this.bindings.get(elementId);
            if (!binding) return;
            
            const {{ element }} = binding;
            
            try {{
                if (property === 'innerHTML') {{
                    // Safe innerHTML with basic sanitization
                    if (typeof value === 'string') {{
                        element.innerHTML = window.nextpySanitizeHTML(value);
                    }} else if (value !== null && typeof value === 'object') {{
                        element.innerHTML = window.nextpySanitizeHTML(JSON.stringify(value));
                    }} else {{
                        element.innerHTML = window.nextpySanitizeHTML(value === null || value === undefined ? '' : String(value));
                    }}
                }} else if (property === 'textContent') {{
                    element.textContent = value !== null && typeof value === 'object'
                        ? JSON.stringify(value)
                        : (value === null || value === undefined ? '' : String(value));
                }} else if (property === 'value') {{
                    // Special handling for input value to ensure it updates
                    element.value = String(value);
                }} else if (property.startsWith('data-') || property.startsWith('aria-')) {{
                    element.setAttribute(property, String(value));
                }} else if (property === 'checked') {{
                    element.checked = !!value;
                }} else if (property === 'disabled') {{
                    element.disabled = !!value;
                }} else if (property === 'className') {{
                    element.className = String(value);
                }} else if (property === 'style') {{
                    if (typeof value === 'object') {{
                        Object.assign(element.style, value);
                    }} else {{
                        element.setAttribute('style', String(value));
                    }}
                }} else if (property in element) {{
                    element[property] = value;
                }}
            }} catch (error) {{
            }}
        }}
        
        setupEventHandlers() {{
            if (!this.element) return;
            
            const eventElements = this.element.querySelectorAll("[data-handler]");
            eventElements.forEach(element => {{
                const handlerName = element.getAttribute("data-handler");
                const eventType = element.getAttribute("data-event") || "click";
                
                if (handlerName) {{
                    this.attachEventHandler(element, eventType, handlerName);
                }}
            }});
        }}
        
        attachEventHandler(element, eventType, handlerName) {{
            const handler = (event) => {{
                try {{
                    // Execute handler using structured actions
                    if (window.executeNextPyActions) {{
                        const actions = window.nextpyComponentHandlers?.[handlerName];
                        if (actions) {{
                            window.executeNextPyActions(actions, this.id);
                        }}
                    }}
                }} catch (error) {{
                    console.error('Handler execution error:', error);
                }}
            }};
            
            element.addEventListener(eventType, handler);
            
            // Store for cleanup
            this.unsubscribers.push(() => {{
                element.removeEventListener(eventType, handler);
            }});
        }}
        
        setupEffects() {{
            if (!this.element) return;
            this.mountEffects = [];
            this.dependentEffects = [];
            const effectEls = this.element.querySelectorAll('[data-effect]');
            effectEls.forEach(effectEl => {{
                const effectJson = effectEl.getAttribute('data-effect');
                if (!effectJson) return;
                try {{
                    const effect = JSON.parse(effectJson);
                    this.runEffect(effect);
                }} catch (e) {{
                    console.error('Failed to parse effect:', e);
                }}
            }});
            const depEls = this.element.querySelectorAll('[data-effect-deps]');
            depEls.forEach(effectEl => {{
                const effectJson = effectEl.getAttribute('data-effect-deps');
                const depsAttr = effectEl.getAttribute('data-deps');
                if (!effectJson) return;
                try {{
                    const effect = JSON.parse(effectJson);
                    const deps = depsAttr ? depsAttr.split(',').map(d => d.trim()) : [];
                    this.registerDependentEffect(effect, deps);
                }} catch (e) {{
                    console.error('Failed to parse dependent effect:', e);
                }}
            }});
        }}
        
        runEffect(effect) {{
            try {{
                if (effect.type === 'FETCH') {{
                    const {{ url, options, dataKey, loadingKey, errorKey }} = effect;
                    if (loadingKey) this.stateManager.set(loadingKey, true);
                    if (errorKey) this.stateManager.set(errorKey, null);
                    fetch(url, options || {{}})
                        .then(resp => {{
                            if (!resp.ok) throw new Error('HTTP ' + resp.status);
                            const ct = resp.headers.get('content-type') || '';
                            return ct.includes('application/json') ? resp.json() : resp.text();
                        }})
                        .then(result => {{
                            if (dataKey) this.stateManager.set(dataKey, result);
                        }})
                        .catch(err => {{
                            if (errorKey) this.stateManager.set(errorKey, err.message || String(err));
                        }})
                        .finally(() => {{
                            if (loadingKey) this.stateManager.set(loadingKey, false);
                        }});
                }} else if (effect.type === 'TIMER') {{
                    const {{ interval, stateKey, incrementBy }} = effect;
                    const timerId = setInterval(() => {{
                        if (stateKey) {{
                            const current = this.stateManager.get(stateKey) || 0;
                            this.stateManager.set(stateKey, current + (incrementBy || 1));
                        }}
                    }}, interval || 1000);
                    this.unsubscribers.push(() => clearInterval(timerId));
                }} else if (effect.type === 'CUSTOM_JS' && effect.code) {{
                    try {{ new Function(effect.code).call(this); }} catch (e) {{ console.error('Custom effect error:', e); }}
                }}
            }} catch (e) {{
                console.error('Effect execution error:', e);
            }}
        }}
        
        registerDependentEffect(effect, deps) {{
            deps.forEach(dep => {{
                const unsub = this.stateManager.subscribe((key) => {{
                    if (key === dep) this.runEffect(effect);
                }});
                this.unsubscribers.push(unsub);
            }});
        }}
        
        updateBindings() {{
            // Update all DOM elements with data-bind attributes
            if (!this.element) {{
                return;
            }}
            
            const boundElements = this.element.querySelectorAll('[data-bind]');
            
            boundElements.forEach(el => {{
                const binding = el.getAttribute('data-bind');
                if (!binding) return;
                
                const [property, stateKey] = binding.split(':');
                const value = this.stateManager.get(stateKey);

                try {{
                    if (property === 'textContent') {{
                        el.textContent = value !== null && typeof value === 'object'
                            ? JSON.stringify(value)
                            : (value === null || value === undefined ? '' : String(value));
                    }} else if (property === 'innerHTML') {{
                        // For innerHTML, convert arrays/objects to JSON for proper display
                        if (Array.isArray(value) || (value !== null && typeof value === 'object')) {{
                            el.innerHTML = window.nextpySanitizeHTML(JSON.stringify(value));
                        }} else {{
                            el.innerHTML = window.nextpySanitizeHTML(value === null || value === undefined ? '' : String(value));
                        }}
                    }} else if (property in el) {{
                        el[property] = value;
                    }}
                }} catch (error) {{
                }}
            }});
        }}
        
        destroy() {{
            this.unsubscribers.forEach(unsub => {{
                try {{
                    if (typeof unsub === 'function') unsub();
                    else if (unsub && typeof unsub === 'object' && unsub.callback) {{
                        const idx = this.stateManager.subscribers.indexOf(unsub.callback);
                        if (idx > -1) this.stateManager.subscribers.splice(idx, 1);
                    }}
                }} catch (error) {{
                }}
            }});
            this.unsubscribers = [];
            this.bindings.clear();
            if (window.nextpyComponents && window.nextpyComponents[this.id]) {{
                delete window.nextpyComponents[this.id];
            }}
        }}
    }}
    
    // Initialize component
    const initialState = {json.dumps(context.initial_state)};
    const component = new Component(componentId, initialState);
    
    // Store component reference for cleanup
    window.nextpyComponents = window.nextpyComponents || {{}};
    window.nextpyComponents[componentId] = component;
    
    // Store handlers for event system
    window.nextpyComponentHandlers = window.nextpyComponentHandlers || {{}};
    window.nextpyComponentHandlers[componentId] = {json.dumps(context.event_handlers)};
    
    // Register refetch and other user-defined functions on the global runtime
    if (window.NextPyActionRuntime) {{
        const _regFuncs = {json.dumps(context.registered_functions)};
        for (const [fname, actionBody] of Object.entries(_regFuncs)) {{
            window.NextPyActionRuntime.functions.set(fname, function() {{
                window.NextPyActionRuntime.executeAction(actionBody, componentId);
            }});
        }}
    }}
    
    // Execute mount actions (e.g. FETCH_DATA for useFetch)
    const _mountActions = {json.dumps(context.mount_actions)};
    if (_mountActions.length > 0 && window.NextPyActionRuntime) {{
        for (const _ma of _mountActions) {{
            if (_ma.type === 'RAW_JS' && _ma.code) {{
                try {{ new Function(_ma.code)(); }} catch(e) {{ console.error('RAW_JS mount action error:', e); }}
            }} else {{
                window.NextPyActionRuntime.executeAction(_ma, componentId);
            }}
        }}
    }}
    
    }}
    
    // Initialize component when DOM is ready
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', initializeComponent);
    }} else {{
        // DOM is already ready - try immediately, then retry if element not found (SPA navigation timing)
        const el = document.getElementById(componentId);
        if (el) {{
            initializeComponent();
        }} else {{
            // Element not found yet - retry with increasing delays (SPA body replacement timing)
            let retries = 0;
            const maxRetries = 10;
            const retryInterval = setInterval(() => {{
                retries++;
                const retryEl = document.getElementById(componentId);
                if (retryEl) {{
                    clearInterval(retryInterval);
                    initializeComponent();
                }} else if (retries >= maxRetries) {{
                    clearInterval(retryInterval);
                    console.warn('Component element not found after retries:', componentId);
                }}
            }}, 50);
        }}
    }}
}})();
            """
        else:
            # Generate script for all components
            scripts = []
            for comp_id in self.contexts:
                scripts.append(self.generate_hydration_script(comp_id))
            return "\n".join(scripts)
    
    def generate_cleanup_script(self, component_id: str) -> str:
        """Generate cleanup script for a component"""
        return f"""
(function() {{
    'use strict';
    
    const componentId = '{component_id}';
    
    if (window.nextpyComponents && window.nextpyComponents[componentId]) {{
        window.nextpyComponents[componentId].destroy();
        delete window.nextpyComponents[componentId];
    }}
    
    if (window.nextpyComponentHandlers && window.nextpyComponentHandlers[componentId]) {{
        delete window.nextpyComponentHandlers[componentId];
    }}
    
}})();
        """
    
    def get_component_context(self, component_id: str) -> Optional[HydrationContext]:
        """Get component context by ID"""
        return self.contexts.get(component_id)
    
    def cleanup_component(self, component_id: str) -> None:
        """Clean up component context"""
        if component_id in self.contexts:
            del self.contexts[component_id]
    
    def generate_html_wrapper(self, component_id: str, html_content: str, state: Dict[str, Any]) -> str:
        """Generate HTML wrapper with hydration script"""
        # Register component with state
        if component_id not in self.contexts:
            self.register_component({
                'name': 'Component',
                'state': state
            })
            registered_id = list(self.contexts.keys())[-1]
            if registered_id != component_id:
                self.contexts[component_id] = self.contexts.pop(registered_id)
                self.contexts[component_id].component_id = component_id
        
        hydration_script = self.generate_hydration_script(component_id)
        
        return f"""
<div id="{component_id}" data-component-id="{component_id}" class="nextpy-component">
    {html_content}
</div>
<script>
{hydration_script}
</script>
        """


# Global hydration engine instance
hydration_engine = HydrationEngine()


def get_hydration_engine() -> HydrationEngine:
    """Get the global hydration engine instance"""
    return hydration_engine
