# NextPy Introspection Module

**Version:** 1.0.0  
**Stability:** Stable (semantic versioning applies)  
**Purpose:** Stable API contract for NextPy Agent

## Overview

The introspection module provides a **stable, versioned API** for the NextPy Agent to inspect and understand NextPy framework internals. This is the **ONLY module** the agent is allowed to depend on from the framework.

## Design Principles

1. **Stability First**: API changes follow semantic versioning. Breaking changes require major version bumps.
2. **Implementation Agnostic**: The agent should not depend on internal framework implementation details.
3. **Type Safety**: All APIs use type hints and return stable data structures.
4. **Serialization Ready**: All data structures can be converted to JSON for agent consumption.
5. **Minimal Surface**: Only expose what the agent needs, not everything the framework does.

## Module Structure

```
nextpy/introspection/
├── __init__.py          # Main API exports
├── ast.py              # AST node inspection
├── components.py       # Component metadata
├── framework.py        # Framework information
├── compiler.py         # Compilation details
└── README.md           # This file
```

## API Reference

### AST Introspection (`ast.py`)

Inspect PSX AST nodes in a stable way.

```python
from nextpy.introspection import get_ast_info, get_node_type, ASTNodeType

# Get comprehensive AST information
info = get_ast_info(psx_node)
print(info.to_dict())

# Get specific information
node_type = get_node_type(psx_node)  # Returns ASTNodeType enum
children = get_node_children(psx_node)  # Returns list of ASTNodeInfo
attributes = get_node_attributes(psx_node)  # Returns dict
```

**Key Types:**
- `ASTNodeType`: Enum of node types (ELEMENT, TEXT, EXPRESSION, etc.)
- `ASTNodeInfo`: Stable container for node information with `to_dict()` method

### Component Introspection (`components.py`)

Inspect PSX components and their metadata.

```python
from nextpy.introspection import get_component_info, ComponentType

# Get component information
info = get_component_info(my_component)
print(info.to_dict())

# Get specific information
props = get_component_props(my_component)
hooks = get_component_hooks(my_component)
```

**Key Types:**
- `ComponentType`: Enum of component types (FUNCTIONAL, CLASS_BASED, HOOKS_BASED)
- `HookType`: Enum of hook types (STATE, EFFECT, REDUCER, etc.)
- `ComponentInfo`: Stable container with name, type, props, hooks, etc.

### Framework Introspection (`framework.py`)

Get framework capabilities and configuration.

```python
from nextpy.introspection import get_framework_info, get_parser_info, get_runtime_info

# Get comprehensive framework information
framework_info = get_framework_info()
print(framework_info.to_dict())

# Get specific information
parser_info = get_parser_info()
runtime_info = get_runtime_info()
```

**Key Types:**
- `ParserType`: Enum of parser types (PSX, JSX, LEGACY)
- `RuntimeType`: Enum of runtime types (SERVER, CLIENT, HYBRID)
- `FrameworkInfo`: Comprehensive framework metadata

### Compiler Introspection (`compiler.py`)

Understand compilation pipeline and targets.

```python
from nextpy.introspection import get_compilation_target, get_client_emit_info

# Get compilation information
comp_info = get_compilation_target()
print(comp_info.to_dict())

# Get client emit information
client_info = get_client_emit_info()
print(client_info.to_dict())
```

**Key Types:**
- `CompilationTarget`: Enum of targets (PYTHON, JAVASCRIPT, HTML)
- `ClientEmitInfo`: Information about client-side code generation

## Versioning Policy

This module follows **semantic versioning**:

- **MAJOR**: Breaking changes to API
- **MINOR**: New features added (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Current Version: 1.0.0

**Stable APIs:**
- All functions in `__init__.py`
- All dataclass structures
- All enum types

**Future Compatibility:**
- New fields may be added to dataclasses (backward compatible)
- New enum values may be added (backward compatible)
- New functions may be added (backward compatible)

## Usage Guidelines for Agent Development

### DO:
- Use only the functions exported from `nextpy.introspection`
- Check version compatibility before using new features
- Handle unknown enum values gracefully
- Use `to_dict()` methods for serialization
- Assume data structures may have additional fields in future versions

### DON'T:
- Import from internal framework modules (e.g., `nextpy.psx.core`)
- Depend on implementation details of returned objects
- Assume enum values are exhaustive
- Access private attributes (starting with `_`)
- Modify returned data structures

## Example: Agent Integration

```python
from nextpy.introspection import (
    get_framework_info,
    get_ast_info,
    get_component_info,
    get_compilation_target,
)

def analyze_nextpy_project():
    """Example agent function using introspection API"""
    
    # Check framework capabilities
    framework = get_framework_info()
    if not framework.capabilities.get("ssr"):
        return "Framework does not support SSR"
    
    # Analyze components
    components = []
    for component in project_components:
        info = get_component_info(component)
        components.append(info.to_dict())
    
    # Analyze AST nodes
    ast_nodes = []
    for node in parsed_psx:
        info = get_ast_info(node)
        ast_nodes.append(info.to_dict())
    
    # Check compilation target
    comp_info = get_compilation_target()
    if comp_info.client_target != "javascript":
        return "Unexpected client target"
    
    return {
        "framework": framework.to_dict(),
        "components": components,
        "ast_nodes": ast_nodes,
        "compilation": comp_info.to_dict(),
    }
```

## Testing

The introspection module includes validation to ensure stability:

```python
# Test that all APIs return serializable data
from nextpy.introspection import get_framework_info

info = get_framework_info()
import json
json.dumps(info.to_dict())  # Should not raise
```

## Migration Guide

### For Future Versions

When upgrading to a new major version:

1. Check the changelog for breaking changes
2. Update enum handling to account for new values
3. Test with your specific use cases
4. Update version compatibility checks

### Example Migration (1.0.0 → 2.0.0)

```python
# Old code (1.0.0)
info = get_component_info(func)
if info.component_type == ComponentType.FUNCTIONAL:
    # ...

# New code (2.0.0) - handle new component types
info = get_component_info(func)
if info.component_type == ComponentType.FUNCTIONAL:
    # ...
elif info.component_type == ComponentType.ASYNC_FUNCTIONAL:  # New type
    # ...
else:
    # Handle unknown future types gracefully
    logger.warning(f"Unknown component type: {info.component_type}")
```

## Support

For issues or questions about the introspection API:
- Check this documentation first
- Review the type hints in source files
- Test with the provided examples
- Report bugs with version information

## Architecture Decision: JavaScript Client Target

The introspection module reflects the architectural decision to target **JavaScript** for client-side compilation:

- `get_client_emit_info()` returns `target=CompilationTarget.JAVASCRIPT`
- `get_runtime_info()` returns `client_target="javascript"`
- Action types are designed for the JavaScript runtime

This decision was based on:
- Existing JS infrastructure in the framework
- DOM-first architecture aligning with JS strengths
- Ecosystem maturity and developer experience
- Performance adequacy for UI workloads

See the main framework documentation for the full analysis.
