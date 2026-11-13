from nextpy.psx import psx, component, register_component


@component
def APIReference(props):
    return psx("""
        <section id="api-reference" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">API Reference</h2>
                <p class="mt-2 text-gray-400">
                    Detailed technical documentation for NextPy modules, components, and utilities.
                </p>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-blue-400">Core Modules</h3>
                <p class="mt-2 text-sm text-blue-300">
                    The main NextPy modules provide the core functionality for building applications.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">nextpy.psx</h3>
                    <p class="mt-2 text-sm text-gray-400">Core PSX functionality for component-based UI</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import component, psx, useState, create_onclick

# Main exports:
# - component: Decorator for creating components
# - psx: Function for parsing PSX syntax
# - useState: Hook for state management
# - create_onclick: Event handler utility
# - interactive_component: Decorator for interactive components</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">nextpy.routing</h3>
                    <p class="mt-2 text-sm text-gray-400">File-based routing and URL handling</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.routing import Router, get_params

# Main exports:
# - Router: Main routing class
# - get_params: Get URL parameters
# - get_query: Get query string parameters
# - redirect: Redirect to another route</pre>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">nextpy.state</h3>
                    <p class="mt-2 text-sm text-gray-400">State management and hooks</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.state import useState, useEffect, useContext

# Main exports:
# - useState: State management hook
# - useEffect: Side effects hook
# - useContext: Context hook
# - useReducer: Reducer hook
# - useRef: Reference hook</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">nextpy.db</h3>
                    <p class="mt-2 text-sm text-gray-400">Database integration and ORM</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.db import Database, Model

# Main exports:
# - Database: Database connection class
# - Model: Base model class
# - Column: Column definition
# - session: Database session</pre>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">nextpy.auth</h3>
                    <p class="mt-2 text-sm text-gray-400">Authentication and authorization</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.auth import SessionAuth, JWTAuth, require_auth

# Main exports:
# - SessionAuth: Session-based authentication
# - JWTAuth: JWT token authentication
# - OAuthProvider: OAuth integration
# - require_auth: Authentication decorator</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">nextpy.cli</h3>
                    <p class="mt-2 text-sm text-gray-400">Command-line interface tools</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># CLI commands:
# nextpy dev          # Start development server
# nextpy build        # Build for production
# nextpy create       # Create new project
# nextpy ai           # Start AI assistant
# nextpy deploy       # Deploy application</pre>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Component API</h3>
                <p class="mt-2 text-sm text-gray-400">
                    Detailed API for PSX components and their lifecycle.
                </p>
                <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">@component
def MyComponent(props):
    # props: Dict[str, Any] - Component properties
    # Returns: PSXElement - Rendered component
    
    # Component lifecycle:
    # 1. Component is called with props
    # 2. State is initialized
    # 3. Effects are run
    # 4. Component is rendered
    # 5. Updates trigger re-renders
    
    return <div>{props.get('children')}</div></pre>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Hooks API</h3>
                <p class="mt-2 text-sm text-gray-400">
                    Complete API reference for React-style hooks in Python.
                </p>
                <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># useState(initial_value)
# Returns: (current_value, setter_function)
[count, setCount] = useState(0)

# useEffect(effect_function, dependencies)
# Returns: None
useEffect(lambda: print("Effect ran"), [count])

# useContext(context)
# Returns: context_value
value = useContext(MyContext)

# useReducer(reducer, initial_state)
# Returns: (state, dispatch_function)
[state, dispatch] = useReducer(reducer, initial_state)

# useRef(initial_value)
# Returns: ref object with .current property
ref = useRef(null)</pre>
            </div>
        </section>
    """)

register_component("APIReference", APIReference)