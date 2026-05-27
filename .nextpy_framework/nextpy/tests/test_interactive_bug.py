#!/usr/bin/env python3
"""
Test script to reproduce interactive_component 'effect' error
"""

import sys
sys.path.insert(0, './.nextpy_framework')

# Test importing interactive_component
print("Testing imports...")

try:
    from nextpy.psx.hydration.decorators import interactive_component
    print("✓ interactive_component imported successfully")
except ImportError as e:
    print(f"✗ Failed to import interactive_component: {e}")

try:
    from nextpy.psx import useState, useEffect
    print("✓ useState and useEffect imported successfully")
except ImportError as e:
    print(f"✗ Failed to import hooks: {e}")

# Test using the decorator
print("\nTesting decorator usage...")

try:
    @interactive_component
    def TestComponent(props=None):
        [count, setCount] = useState(0)
        
        def _effect():
            print("Component mounted")
            
        useEffect(_effect, [])
        
        def handle_click():
            setCount(count + 1)
        
        return "<div><p>Count: {count}</p><button onClick={handle_click}>Click me</button></div>"
    
    print("✓ Component defined successfully")
    
    # Try to render it
    result = TestComponent()
    print(f"✓ Component rendered: {type(result)}")
    
except Exception as e:
    print(f"✗ Error in component: {e}")
    import traceback
    traceback.print_exc()
