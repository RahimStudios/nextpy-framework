# NextPy Hydration Engine - Complete Documentation

## Overview

The **Hydration Engine** is a client-side runtime system that enables true interactivity for NextPy PSX components. It bridges the gap between server-side Python rendering and client-side JavaScript interactivity.

## Architecture

### How It Works

1. **Server-Side**: Python component is rendered to HTML with initial state
2. **Hydration Data**: State and event handlers are serialized and embedded in the HTML
3. **Client-Side Initialization**: JavaScript loaded and initializes component
4. **Reactive Updates**: State changes trigger DOM updates without page reload

### Components

- **HydrationEngine**: Core system for generating client-side code
- **ComponentHydrator**: Extracts metadata from Python components
- **Interactive Decorator**: Wraps components with hydration support
- **Client Runtime**: JavaScript system running in the browser

## Quick Start

### 1. Using the Interactive Decorator

```python
from nextpy.psx import component, useState, create_onclick
from nextpy.psx.hydration import interactive_component

@interactive_component
def Counter(props=None):
    [count, setCount] = useState(0)
    
    return psx("""
        <div>
            <h1>Count: {count}</h1>
            <button onclick={lambda e: setCount(count + 1)}>
                Increment
            </button>
        </div>
    """)
```

### 2. Enable Global Hydration

To enable hydration for all components in your app:

```python
# In your main app file
from nextpy.psx.hydration import enable_hydration_globally

enable_hydration_globally()

# Now all @component decorated functions are interactive
@component
def MyComponent(props=None):
    # This will automatically be interactive!
    pass
```

### 3. Create an Interactive Page

```python
from nextpy.psx.hydration import create_interactive_page

# Get your component
component_html = render_component()
hydration_script = get_hydration_script()

# Create complete page
page_html = create_interactive_page(component_html, hydration_script,
                                   title="My App")
```

## Features

### 1. Automatic State Extraction

The hydration engine automatically extracts state from `useState()` calls:

```python
@interactive_component
def Component(props=None):
    [count, setCount] = useState(0)          # → state.count = 0
    [name, setName] = useState("John")       # → state.name = "John"
    [items, setItems] = useState([])         # → state.items = []
```

### 2. Event Handler Binding

Event handlers are automatically converted from Python to JavaScript:

```python
# Python event handler
onclick={lambda e: setCount(count + 1)}

# Converted to JavaScript
state.set("count", count + 1)
```

### 3. Dynamic DOM Updates

State changes automatically update the DOM:

```python
# When setState is called...
state.set("count", 5)

# ... any elements bound to that state update automatically
# <h1>Count: 5</h1>  ← Updates in real-time
```

### 4. Effect Management

Use effects for side effects and async operations:

```python
@interactive_component
def Component(props=None):
    [data, setData] = useState(None)
    
    def fetchData():
        # This runs on mount
        fetch('/api/data').then(r => r.json()).then(d => setData(d))
    
    useEffect(fetchData, [])  # Empty dependency array = run once
```

## API Reference

### Interactive Component Decorator

```python
@interactive_component
def MyComponent(props=None):
    # Component code here
    pass
```

Returns an `InteractiveComponentResult` with:
- `.html`: The rendered HTML with hydration data
- `.script`: The JavaScript hydration script
- `.is_interactive`: Boolean flag

### Hydration Functions

#### `hydrate_component(component_func, props, html)`

Manually hydrate a component.

```python
from nextpy.psx.hydration import hydrate_component

hydrated_html, script = hydrate_component(MyComponent, {}, html_string)
```

#### `create_interactive_page(html, script, title)`

Create a complete HTML page with hydration.

```python
from nextpy.psx.hydration import create_interactive_page

full_page = create_interactive_page(component_html, script, "My Page")
```

### Client-Side API

#### `NextPyRuntime.createComponent(componentId, initialState)`

Create a component instance on the client.

```javascript
const component = NextPyRuntime.createComponent('psx_component_1', {
    count: 0,
    name: 'John'
});
```

#### `component.stateManager.set(path, value)`

Set a state value.

```javascript
// Set top-level state
component.stateManager.set('count', 5);

// Set nested state
component.stateManager.set('user.name', 'Jane');
```

#### `component.bind(elementId, property, statePath)`

Bind an element property to state.

```javascript
component.bind('count-display', 'textContent', 'count');
```

#### `component.on(eventName, elementId, handler)`

Register an event handler.

```javascript
component.on('click', 'increment-btn', function(event, state) {
    state.set('count', state.get('count') + 1);
});
```

## Advanced Usage

### Custom Event Handlers

```python
@interactive_component
def Component(props=None):
    [count, setCount] = useState(0)
    
    def handleCustomClick(e):
        currentCount = getState('count')
        setCount(currentCount * 2)
    
    return psx("""
        <button onclick={handleCustomClick}>
            Double Count
        </button>
    """)
```

### Form Handling

```python
@interactive_component
def Form(props=None):
    [formData, setFormData] = useState({"name": "", "email": ""})
    [errors, setErrors] = useState({})
    
    def handleChange(fieldName, value):
        newFormData = formData.copy()
        newFormData[fieldName] = value
        setFormData(newFormData)
    
    def handleSubmit(e):
        # Validate
        if not formData['name']:
            setErrors({'name': 'Name required'})
            return
        
        # Submit
        # ... send to server
```

### Conditional Rendering

```python
@interactive_component
def Component(props=None):
    [isOpen, setIsOpen] = useState(False)
    
    return psx("""
        {if isOpen:
            <div class="modal">Dropdown content</div>
        {/if}}
        
        <button onclick={lambda e: setIsOpen(not isOpen)}>
            Toggle
        </button>
    """)
```

## Performance Optimization

### 1. Use Key Attributes

For lists, always use the `key` attribute:

```python
{for item in items:
    <div key={item.id} class="item">
        {item.name}
    </div>
}
```

### 2. Memoization

Use `useMemo` to prevent unnecessary recalculations:

```python
from nextpy.psx import useMemo

@interactive_component
def Component(props=None):
    [count, setCount] = useState(0)
    
    # This only recalculates when count changes
    computed = useMemo(lambda: count * 2, [count])
```

### 3. Callback Optimization

Use `useCallback` to memoize event handlers:

```python
from nextpy.psx import useCallback

@interactive_component
def Component(props=None):
    [count, setCount] = useState(0)
    
    # This handler is only created once
    handleIncrement = useCallback(
        lambda e: setCount(count + 1),
        [count]
    )
```

## Debugging

### Enable Debug Mode

```javascript
// In browser console
window.NextPyRuntime.DEBUG = true;
```

### Inspect Component State

```javascript
// Get component
const component = NextPyRuntime.components.get('psx_component_1');

// Log current state
console.log(component.stateManager.state);

// Subscribe to changes
component.stateManager.subscribe((newState) => {
    console.log('State changed:', newState);
});
```

### View Component History

The hydration engine keeps a history of state changes for undo/redo:

```javascript
// Undo last change
component.stateManager.undo();

// Redo
component.stateManager.redo();
```

## Best Practices

1. **Keep State Minimal**: Only store data that affects the UI
2. **Use Composition**: Break complex components into smaller ones
3. **Validate Input**: Always validate user input before state updates
4. **Handle Errors**: Wrap event handlers in try-catch
5. **Performance**: Use keys in lists and memoize expensive computations
6. **Accessibility**: Add proper labels and ARIA attributes
7. **Mobile-Friendly**: Test on various screen sizes

## Troubleshooting

### State Not Updating

**Problem**: `setCount()` doesn't update the UI

**Solution**: Make sure you're using the hydration decorator:
```python
@interactive_component  # ← Required!
def Component(props=None):
    pass
```

### Event Handlers Not Firing

**Problem**: Button clicks don't trigger handlers

**Solution**: Check that elements have proper IDs and handlers are registered:
```python
<button onclick={myHandler} id="my-button">Click</button>
```

### JavaScript Errors in Console

**Problem**: "NextPyRuntime is not defined"

**Solution**: Make sure the hydration script is loaded before components:
```html
<script src="hydration-runtime.js"></script>
<div id="app"><!-- Your components --></div>
```

## Migration from Plain Components

### Before (No Interactivity)
```python
@component
def Counter(props=None):
    [count, setCount] = useState(0)
    return psx(...)  # State changes don't work
```

### After (With Interactivity)
```python
@interactive_component  # ← Just add this!
def Counter(props=None):
    [count, setCount] = useState(0)
    return psx(...)  # State changes now work!
```

## Future Enhancements

Planned features for the hydration engine:

- [ ] Server-side rendering with client hydration
- [ ] WebSocket support for real-time updates
- [ ] Automatic code splitting
- [ ] DevTools browser extension
- [ ] Time-travel debugging
- [ ] Performance monitoring
- [ ] Server mutation support
- [ ] Optimistic updates

## Examples

See the `/pages/hydration_example.py` for complete working examples.

## Support

For issues, feature requests, or questions:

1. Check the troubleshooting section above
2. Review the examples in `/pages/hydration_example.py`
3. Check browser console for JavaScript errors
4. Enable debug mode for detailed logging

---

**NextPy Hydration Engine v1.0**
Making interactive web apps with Python JSX!
