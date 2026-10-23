# NextPy Migration Guide

This guide helps you migrate from legacy systems to NextPy v5.0.0.

## Table of Contents
1. [Migrating from Legacy Hooks](#migrating-from-legacy-hooks)
2. [Migrating from JSX to PSX](#migrating-from-jsx-to-psx)
3. [Migrating Event Handlers](#migrating-event-handlers)
4. [Migrating Legacy Components](#migrating-legacy-components)
5. [Breaking Changes](#breaking-changes)
6. [Common Issues](#common-issues)

---

## Migrating from Legacy Hooks

### Before (Legacy Hooks)
```python
from nextpy.hooks import useState, useEffect
from nextpy.hooks_provider import HooksProvider

@HooksProvider
def MyComponent():
    [count, setCount] = useState(0)
    
    useEffect(lambda: print("Mounted"), [])
    
    return psx("<div>{count}</div>")
```

### After (PSX Hooks)
```python
from nextpy.psx import component, useState, useEffect

@component
def MyComponent(props=None):
    [count, setCount] = useState(0)
    
    def on_mount():
        print("Mounted")
    
    useEffect(on_mount, [])
    
    return psx("<div>{count}</div>")
```

**Key Changes:**
- Import hooks from `nextpy.psx` instead of `nextpy.hooks`
- Use `@component` decorator instead of `@HooksProvider`
- Pass named functions to `useEffect` instead of lambdas

---

## Migrating from JSX to PSX

### Before (Legacy JSX)
```python
from nextpy.jsx import jsx
from nextpy.jsx_transformer import JSXTransformer

transformer = JSXTransformer()

def MyComponent():
    return jsx"""
        <div class="container">
            <h1>Hello World</h1>
        </div>
    """
```

### After (PSX)
```python
from nextpy.psx import component, psx

@component
def MyComponent(props=None):
    return psx("""
        <div class="container">
            <h1>Hello World</h1>
        </div>
    """)
```

**Key Changes:**
- Use `psx()` function instead of `jsx()` or `jsx_transformer`
- Import from `nextpy.psx` module
- Use `@component` decorator for better state management

---

## Migrating Event Handlers

### Before (Inline Lambdas - DEPRECATED)
```python
from nextpy.psx import component, useState, create_onclick

@component
def Counter(props=None):
    [count, setCount] = useState(0)
    handle_click = create_onclick(lambda e: setCount(count + 1))
    
    return psx("""
        <button create_onclick={handle_click}>
            Count: {count}
        </button>
    """)
```

### After (Named Handlers - RECOMMENDED)
```python
from nextpy.psx import component, useState

@component
def Counter(props=None):
    [count, setCount] = useState(0)
    
    def handle_increment(e):
        setCount(count + 1)
    
    return psx("""
        <button onclick={handle_increment}>
            Count: {count}
        </button>
    """)
```

**Key Changes:**
- Use named handler functions instead of lambdas
- Use `onclick` attribute instead of `create_onclick`
- Handlers are automatically extracted and converted to JavaScript

**Why This Change?**
- Better debugging (named functions appear in stack traces)
- Improved hydration (easier to extract and convert)
- Cleaner code structure
- Better performance (function reuse)

---

## Migrating Legacy Components

### Before (Legacy Components - DELETED)
The following components have been removed:
- `nextpy.components.feedback` - Use custom form feedback
- `nextpy.components.loader` - Create custom loading states
- `nextpy.components.toast` - Use custom notification system
- `nextpy.components.visual` - Use Tailwind CSS directly

### After (Custom Components)
```python
from nextpy.psx import component, useState

@component
def Toast(props=None):
    props = props or {}
    message = props.get("message", "")
    variant = props.get("variant", "info")
    
    colors = {
        "info": "bg-blue-500",
        "success": "bg-green-500",
        "error": "bg-red-500",
        "warning": "bg-yellow-500"
    }
    
    return psx(f"""
        <div class="{colors[variant]} text-white px-4 py-2 rounded">
            {message}
        </div>
    """)
```

---

## Breaking Changes

### 1. Removed Modules
- `nextpy.hooks` → Use `nextpy.psx` hooks
- `nextpy.hooks_provider` → Use `@component` decorator
- `nextpy.jsx` → Use `nextpy.psx`
- `nextpy.jsx_transformer` → Use `nextpy.psx` compiler
- `nextpy.jsx_preprocessor` → Not needed with PSX

### 2. Deleted Components
- `nextpy.components.feedback`
- `nextpy.components.loader`
- `nextpy.components.toast`
- `nextpy.components.visual`

### 3. Deleted Debug Files
- `nextpy.components.debug.AutoDebug` → Use `AutoDebug_v3`
- `nextpy.components.debug.DebugIcon` → Use `AutoDebug_v3`
- `nextpy.components.debug.DebugIconFixed` → Use `AutoDebug_v3`

### 4. Event Handler Syntax
**Before:**
```python
onclick={lambda e: setCount(count + 1)}
create_onclick={handle_click}
```

**After:**
```python
def handle_increment(e):
    setCount(count + 1)

onclick={handle_increment}
```

### 5. File Structure Changes
- Demo pages moved from `pages/` to `examples/`
- Historical documentation moved to `docs/archive/`
- Hydration documentation moved to `docs/history/`

---

## Common Issues

### Issue: "NextPyRuntime is not defined"
**Cause:** Hydration script not embedded in HTML

**Solution:** Use `@interactive_component` decorator:
```python
from nextpy.psx.hydration import interactive_component

@interactive_component
def MyComponent(props=None):
    # Your component code
    pass
```

### Issue: Event handlers not firing
**Cause:** Using inline lambdas instead of named functions

**Solution:** Use named handler functions:
```python
# ❌ Wrong
onclick={lambda e: setCount(count + 1)}

# ✅ Correct
def handle_increment(e):
    setCount(count + 1)

onclick={handle_increment}
```

### Issue: State not updating UI
**Cause:** Not using `@component` or `@interactive_component` decorator

**Solution:** Add decorator:
```python
@component  # or @interactive_component
def MyComponent(props=None):
    [count, setCount] = useState(0)
    # ...
```

### Issue: Import errors after migration
**Cause:** Importing from deleted modules

**Solution:** Update imports:
```python
# ❌ Old imports
from nextpy.hooks import useState
from nextpy.jsx import jsx

# ✅ New imports
from nextpy.psx import component, useState, psx
```

---

## Migration Checklist

- [ ] Update all hook imports from `nextpy.hooks` to `nextpy.psx`
- [ ] Replace `@HooksProvider` with `@component` decorator
- [ ] Convert all inline lambda handlers to named functions
- [ ] Replace `create_onclick` with `onclick` attribute
- [ ] Remove usage of deleted components (feedback, loader, toast, visual)
- [ ] Create custom replacements for deleted components
- [ ] Update debug components to use `AutoDebug_v3`
- [ ] Move demo pages to `examples/` directory
- [ ] Test all interactive components
- [ ] Verify event handlers work correctly
- [ ] Check console for JavaScript errors

---

## Need Help?

If you encounter issues during migration:

1. Check the [Documentation](.nextpy_framework/nextpy/docs/COMPREHENSIVE_GUIDE.md)
2. Review [Hydration Engine Guide](.nextpy_framework/nextpy/docs/history/HYDRATION_ENGINE_GUIDE.md)
3. Check examples in `examples/` directory
4. Enable debug mode: `window.NextPyRuntime.DEBUG = true`
5. Review browser console for errors

---

**NextPy v5.0.0 Migration Guide**
Last Updated: October 22, 2026
