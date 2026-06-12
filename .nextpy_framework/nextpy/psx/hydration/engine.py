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
        
        context = HydrationContext(
            component_id=component_id,
            component_name=component_data.get('name', 'Component'),
            initial_state=component_data.get('state', {}),
            event_handlers=component_data.get('handlers', {}),
            use_effects=component_data.get('effects', []),
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
            const oldValue = this.state[key];
            this.state[key] = value;
            console.log('StateManager.set:', key, '=', value, '(old:', oldValue, ')');
            
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
            const elementId = element.id || element.getAttribute('data-element-id');
            
            if (!elementId) return;
            
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
        }}
        
        updateBinding(elementId, property, value) {{
            const binding = this.bindings.get(elementId);
            if (!binding) return;
            
            const {{ element }} = binding;
            
            try {{
                if (property === 'innerHTML') {{
                    // Safe innerHTML with basic sanitization
                    if (typeof value === 'string') {{
                        element.innerHTML = value.replace(/<script[^>]*>.*?<\\/script>/gi, '');
                    }} else {{
                        element.innerHTML = String(value);
                    }}
                }} else if (property === 'textContent') {{
                    element.textContent = String(value);
                }} else if (property in element) {{
                    element[property] = value;
                }}
            }} catch (error) {{
                console.error('Binding update error:', error);
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
            // Effects setup would go here
            // For now, we'll just log that effects are being set up
            console.log('Effects setup for component:', this.id);
        }}
        
        updateBindings() {{
            // Update all DOM elements with data-bind attributes
            if (!this.element) {{
                console.error('updateBindings: No element found for component:', this.id);
                return;
            }}
            
            console.log('updateBindings: Starting for component:', this.id, 'with state:', this.stateManager.state);
            
            const boundElements = this.element.querySelectorAll('[data-bind]');
            console.log('updateBindings: Found', boundElements.length, 'elements with data-bind');
            
            boundElements.forEach(el => {{
                const binding = el.getAttribute('data-bind');
                if (!binding) return;
                
                const [property, stateKey] = binding.split(':');
                const value = this.stateManager.get(stateKey);

                console.log('updateBindings: Updating element with binding:', binding, 'value:', value);

                try {{
                    if (property === 'textContent') {{
                        el.textContent = String(value);
                    }} else if (property === 'innerHTML') {{
                        // For innerHTML, convert arrays/objects to JSON for proper display
                        if (Array.isArray(value) || typeof value === 'object') {{
                            el.innerHTML = JSON.stringify(value);
                        }} else {{
                            el.innerHTML = String(value);
                        }}
                    }} else if (property in el) {{
                        el[property] = value;
                    }}
                }} catch (error) {{
                    console.error('Binding update error:', error);
                }}
            }});
            
            console.log('Updated', boundElements.length, 'data bindings');
        }}
        
        destroy() {{
            // Cleanup all subscriptions
            this.unsubscribers.forEach(unsub => {{
                try {{
                    unsub();
                }} catch (error) {{
                    console.error('Cleanup error:', error);
                }}
            }});
            this.unsubscribers = [];
            this.bindings.clear();
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
    
    console.log('[NextPy] Component hydrated:', componentId);
    }}
    
    // Initialize component when DOM is ready
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', initializeComponent);
    }} else {{
        // DOM is already ready
        initializeComponent();
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
    
    console.log('[NextPy] Component cleaned up:', componentId);
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
            # Update the component ID to match the registered one
            registered_id = list(self.contexts.keys())[-1]
            print('this is is', registered_id)
            if registered_id != component_id:
                # Move the context to the correct ID
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
