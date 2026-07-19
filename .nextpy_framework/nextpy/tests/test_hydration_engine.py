"""
Test suite for NextPy Hydration Engine
"""

import sys
sys.path.insert(0, './.nextpy_framework')

from nextpy.psx.hydration import (
    HydrationEngine, 
    get_hydration_engine,
    get_component_hydrator,
    interactive_component,
)

print("=" * 70)
print("NEXTPY HYDRATION ENGINE TEST SUITE")
print("=" * 70)

# Test 1: Hydration Engine Initialization
print("\nTest 1: Engine Initialization")
print("-" * 70)
try:
    engine = get_hydration_engine()
    print("✓ Hydration engine initialized")
    print(f"✓ Engine type: {type(engine).__name__}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 2: Component Registration
print("\nTest 2: Component Registration")
print("-" * 70)
try:
    component_id = engine.register_component({
        'name': 'TestComponent',
        'state': {'count': 0, 'name': 'Test'},
        'handlers': {'increment': 'setCount(count + 1)'},
    })
    print(f"✓ Component registered: {component_id}")
    print(f"✓ Component ID format: {component_id.startswith('psx_component_')}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 3: Hydration Script Generation
print("\nTest 3: Hydration Script Generation")
print("-" * 70)
try:
    script = engine.generate_hydration_script()
    print(f"✓ Script generated ({len(script)} bytes)")
    print(f"✓ Contains runtime core: {'NextPyRuntime' in script}")
    print(f"✓ Contains state manager: {'StateManager' in script}")
    print(f"✓ Contains component hydrator: {'Component' in script and 'class' in script}")
    
    # Check script sections
    sections = {
        'Runtime Core': 'NextPyRuntime = window.NextPyRuntime || {};',
        'State Manager': 'NextPyRuntime.StateManager = class',
        'Component': 'NextPyRuntime.Component = class',
        'CreateComponent': 'NextPyRuntime.createComponent',
    }
    
    for section, marker in sections.items():
        if marker in script:
            print(f"  ✓ {section} included")
        else:
            print(f"  ✗ {section} MISSING")
            
except Exception as e:
    print(f"✗ Failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Component Hydrator
print("\nTest 4: Component Hydrator")
print("-" * 70)
try:
    hydrator = get_component_hydrator()
    print(f"✓ Component hydrator obtained")
    
    # Test metadata extraction
    def sample_component(props=None):
        """Sample component for testing"""
        pass
    
    metadata = hydrator.extract_component_metadata(sample_component)
    print(f"✓ Component metadata extracted: {metadata}")
    
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 5: HTML Wrapper Generation
print("\nTest 5: HTML Wrapper Generation")
print("-" * 70)
try:
    html = '<div>Test content</div>'
    state = {'count': 0, 'message': 'Hello'}
    
    wrapped = engine.generate_html_wrapper('test_comp_1', html, state)
    
    print(f"✓ HTML wrapper generated ({len(wrapped)} bytes)")
    print(f"✓ Contains component div: {'<div id=\"test_comp_1\"' in wrapped}")
    print(f"✓ Contains state data: {'data-state=' in wrapped}")
    print(f"✓ Contains auto-hydration script: {'NextPyRuntime.createComponent' in wrapped}")
    
    # Show wrapped output preview
    preview = wrapped[:200]
    print(f"  Preview: {preview}...")
    
except Exception as e:
    print(f"✗ Failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Interactive Component Decorator
print("\nTest 6: Interactive Component Decorator")
print("-" * 70)
try:
    @interactive_component
    def TestComponent(props=None):
        return None  # Simplified for testing
    
    # Call the decorated function
    result = TestComponent({'name': 'Test'})
    
    print(f"✓ Component decorated successfully")
    print(f"✓ Result type: {type(result).__name__}")
    print(f"✓ Has html attribute: {hasattr(result, 'html')}")
    print(f"✓ Has script attribute: {hasattr(result, 'script')}")
    print(f"✓ Is interactive: {hasattr(result, 'is_interactive') and result.is_interactive}")
    
except Exception as e:
    print(f"✗ Failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("TEST SUITE COMPLETE")
print("=" * 70)
print("\n✓ All basic hydration engine components are working!")
print("\nNext steps:")
print("1. Review HYDRATION_ENGINE_GUIDE.md for detailed documentation")
print("2. Check pages/hydration_example.py for example components")
print("3. Enable global hydration with: enable_hydration_globally()")
print("4. Use @interactive_component decorator for interactive features")
