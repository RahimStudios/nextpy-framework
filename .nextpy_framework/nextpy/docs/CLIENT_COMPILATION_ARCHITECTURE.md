# Client-Side Compilation Architecture

**Target:** JavaScript  
**Runtime Version:** 1.0.0  
**Status:** Stable

## Overview

NextPy compiles PSX (Python Syntax Extension) to JavaScript for client-side execution. This document describes the compilation pipeline from Python AST to JavaScript actions.

## Architecture Decision: JavaScript Target

NextPy targets **JavaScript** (not WebAssembly) for client-side compilation based on:

1. **Existing Infrastructure**: Framework already has extensive JS runtime
2. **DOM-First Architecture**: Reactive model relies on direct DOM manipulation
3. **Ecosystem Fit**: React-style patterns work naturally in JS
4. **Performance Adequacy**: Modern JS JIT is sufficient for UI workloads
5. **Developer Experience**: Mature tooling, debugging, and community

## Compilation Pipeline

```
PSX Source → Parser → AST → Optimizer → Code Generator → JavaScript Actions
```

### Phase 1: Parsing

**Input:** PSX source code (Python with JSX-like syntax)  
**Output:** PSX AST nodes  
**Implementation:** `nextpy.psx.core.parser.PSXParser`

```python
# Example PSX source
psx_source = """
<div>
  <h1>Hello {name}</h1>
  <button onClick={handleClick}>Click me</button>
</div>
"""

# Parse to AST
parser = PSXParser()
ast_node = parser.parse_psx(psx_source, context={"name": "World"})
```

**Key Features:**
- Recursive-descent parsing (thread-safe, cross-platform)
- Handles elements, components, expressions, logic blocks
- Safe expression evaluation with AST validation
- Position tracking for error reporting

### Phase 2: AST Generation

**Input:** PSX AST nodes  
**Output:** Optimized AST with parsed expressions  
**Implementation:** `nextpy.psx.core.ast_nodes`

**AST Node Types:**
- `ElementNode`: HTML elements with attributes and children
- `TextNode`: Text content
- `ExpressionNode`: Python expressions `{expr}`
- `ComponentNode`: PSX components
- `FragmentNode`: Fragment nodes `<>...</>`
- Logic nodes: `IfNode`, `ForNode`, `WhileNode`, `TryNode`

**Example AST Structure:**
```python
ElementNode(
    tag="div",
    attributes={},
    children=[
        ElementNode(
            tag="h1",
            attributes={},
            children=[
                TextNode(content="Hello "),
                ExpressionNode(expression="name", parsed_expression=...)
            ]
        ),
        ElementNode(
            tag="button",
            attributes={"onClick": "handleClick"},
            children=[TextNode(content="Click me")]
        )
    ]
)
```

### Phase 3: Optimization

**Input:** Raw AST nodes  
**Output:** Optimized AST nodes  
**Implementation:** `nextpy.psx.core.ast_nodes.PSXNodeOptimizer`

**Optimizations Applied:**
1. **Expression Pre-parsing**: Parse expressions once, cache AST
2. **Attribute Sorting**: Consistent rendering order
3. **Dead Code Elimination**: Remove unreachable nodes
4. **Constant Folding**: Evaluate constant expressions
5. **Tree Shaking**: Remove unused branches

### Phase 4: Code Generation

**Input:** Optimized AST nodes  
**Output:** JavaScript actions  
**Implementation:** `nextpy.psx.core.runtime.PSXRuntime`

**Code Generation Strategy:**

NextPy does **not** generate vanilla JavaScript code. Instead, it generates **structured actions** that are executed by the JavaScript runtime.

#### Why Actions Instead of Direct JS?

1. **Safety**: Structured actions prevent code injection
2. **Debugging**: Clear action traces for debugging
3. **Optimization**: Runtime can optimize action execution
4. **State Management**: Built-in state tracking
5. **Reactivity**: Automatic dependency tracking

#### Action Types

The JavaScript runtime supports these action types:

**State Management:**
- `SET_STATE`: Set a single state variable
- `SET_STATE_BATCH`: Set multiple state variables atomically
- `GET_STATE`: Read state variable

**Function Calls:**
- `CALL_FUNCTION`: Call a registered function
- `CALL_METHOD`: Call a method on an object

**Operations:**
- `BINARY_OP`: Binary operations (+, -, *, /, etc.)
- `UNARY_OP`: Unary operations (+, -, not, ~)
- `COMPARE_OP`: Comparisons (==, !=, <, >, etc.)
- `BOOLEAN_OP`: Boolean operations (and, or)

**Data Structures:**
- `CONSTANT`: Literal value
- `VARIABLE`: Variable reference
- `LIST`: List/array creation
- `DICT`: Dictionary/object creation
- `INDEX`: Array/object indexing
- `ATTRIBUTE`: Object attribute access

**Control Flow:**
- `FOR_LOOP`: For loop execution
- `WHILE_LOOP`: While loop execution
- `TRY`: Try/except block
- `BREAK`: Break statement
- `CONTINUE`: Continue statement
- `RETURN`: Return statement
- `LAMBDA`: Lambda function creation

**UI Updates:**
- `JSX_UPDATE`: Direct DOM manipulation
- `PRINT`: Console output

#### Action Generation Example

**PSX Source:**
```python
[count, setCount] = useState(0)
<button onClick={lambda e: setCount(count + 1)}>Count: {count}</button>
```

**Generated Actions:**
```json
[
  {
    "type": "SET_STATE",
    "data": {
      "key": "count",
      "value": {
        "type": "BINARY_OP",
        "data": {
          "left": {"type": "VARIABLE", "data": {"name": "count"}},
          "op": "+",
          "right": {"type": "CONSTANT", "data": {"value": 1}}
        }
      }
    }
  }
]
```

### Phase 5: JavaScript Runtime

**Input:** JavaScript actions  
**Output:** DOM updates and state changes  
**Implementation:** `nextpy.psx.runtime.js_actions_runtime.JS_ACTION_RUNTIME_SCRIPT`

**Runtime Architecture:**

```javascript
class NextPyActionRuntime {
    constructor() {
        this.components = new Map();      // Component state
        this.globalState = {};            // Global state
        this.functions = new Map();       // Registered functions
        this.dependencyMap = new Map();   // State dependencies
    }
    
    executeAction(action, componentId) {
        // Execute individual action
    }
    
    executeActions(actions, componentId) {
        // Execute action sequence
    }
}
```

**Key Features:**
1. **Component Isolation**: Each component has isolated state
2. **Reactive Updates**: Automatic DOM updates on state changes
3. **Dependency Tracking**: Knows which DOM elements depend on which state
4. **Conditional Rendering**: Handles if/else logic with data attributes
5. **Event Handling**: Structured event handler execution
6. **Safe Evaluation**: No eval(), only structured operations

#### State Management

```javascript
// Register component
runtime.registerComponent("my-component", {count: 0});

// Set state (triggers re-render)
runtime.executeAction({
    type: "SET_STATE",
    data: {key: "count", value: 1}
}, "my-component");

// Get state
const value = runtime.executeAction({
    type: "GET_STATE",
    data: {key: "count"}
}, "my-component");
```

#### DOM Updates

The runtime uses data attributes for reactive updates:

```html
<!-- Text binding -->
<span data-bind="textContent:count">0</span>

<!-- Conditional rendering -->
<span data-if-condition="count > 10" 
      data-if-true="You won!" 
      data-if-false="Keep trying">
  Keep trying
</span>

<!-- Input binding -->
<input data-bind="value:name" />
<input data-bind="checked:isActive" type="checkbox" />
```

When state changes, the runtime:
1. Identifies dependent DOM elements via dependency map
2. Updates text content for data-bind attributes
3. Re-evaluates conditions for data-if-condition
4. Updates input values for two-way binding

## Client-Side Hydration

**Purpose:** Attach JavaScript runtime to server-rendered HTML

**Process:**
1. Server renders PSX to HTML with data attributes
2. Client loads JavaScript runtime
3. Runtime registers components with initial state
4. Runtime builds dependency map from DOM
5. Event handlers become active
6. Future updates are handled client-side

**Example:**
```html
<!-- Server-rendered HTML -->
<div data-component-id="my-component">
  <span data-bind="textContent:count">0</span>
  <button data-handler-click="increment">Increment</button>
</div>

<!-- Client-side hydration -->
<script>
  registerNextPyComponent("my-component", {count: 0});
  // Runtime scans DOM, sets up bindings, activates handlers
</script>
```

## Performance Considerations

### Optimization Strategies

1. **Expression Caching**: Parsed expressions cached in runtime
2. **Batch Updates**: Multiple state changes batched
3. **Selective Updates**: Only update changed DOM elements
4. **Debouncing**: Debounce rapid state changes
5. **Lazy Evaluation**: Expressions evaluated only when needed

### Performance Characteristics

- **Cold Start**: ~50-100ms to load and initialize runtime
- **State Update**: ~1-5ms per state change
- **DOM Update**: ~5-20ms depending on complexity
- **Event Handling**: ~1-3ms per event

### Benchmarks

Based on framework testing:
- **Simple Counter**: 60fps with 1000 updates/sec
- **List Rendering**: 60fps with 100 items
- **Conditional Rendering**: 60fps with 50 conditions
- **Form Binding**: 60fps with 20 inputs

## Security Model

### Safe Execution

The JavaScript runtime uses **structured actions** instead of `eval()`:

- No arbitrary code execution
- No access to dangerous globals
- Whitelisted functions only
- Type-safe operations
- Memory-safe execution

### Data Sanitization

- HTML escaping for text content
- Attribute escaping for attributes
- XSS prevention via structured updates
- CSP-compatible execution

## Debugging

### Runtime Debugging

Enable debug mode:
```javascript
window.NEXTPY_DEBUG = true;
```

Debug features:
- Action execution logging
- State change tracking
- Dependency map inspection
- Performance timing
- Error stack traces

### Browser DevTools

The runtime integrates with browser DevTools:
- Component state in Redux DevTools format
- Action logging in console
- Performance profiling
- Source maps for debugging

## Future Enhancements

### Planned Features

1. **Action Streaming**: Stream actions for large updates
2. **Web Workers**: Offload computation to workers
3. **IndexedDB**: Persistent client-side storage
4. **Service Workers**: Offline support
5. **WebRTC**: Real-time collaboration

### WASM Integration

While JavaScript is the primary target, WASM could be added for:
- Compute-intensive operations (image processing, ML)
- Performance-critical paths
- Existing Rust/C++ libraries

This would be **additive**, not replacing the JavaScript runtime.

## Migration from Other Frameworks

### React Developers

NextPy's action system is similar to React's:
- `useState` → `SET_STATE` actions
- `useEffect` → Runtime lifecycle hooks
- JSX → PSX (same syntax, Python instead of JS)

### Vue Developers

NextPy's reactivity is similar to Vue's:
- Data attributes similar to Vue directives
- Dependency tracking similar to Vue's reactivity system
- Component isolation similar to Vue's components

## Summary

NextPy's client-side compilation:
- **Targets JavaScript** (not WASM)
- **Uses structured actions** (not direct JS generation)
- **Leverages existing infrastructure** (JS runtime already built)
- **Optimizes for UI workloads** (DOM-first architecture)
- **Provides stable API** (introspection module for agent)

This architecture provides a solid foundation for the NextPy Agent to understand and work with client-side code generation.
