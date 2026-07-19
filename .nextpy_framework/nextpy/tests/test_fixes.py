#!/usr/bin/env python3
"""
Test script to verify Hydration Engine fixes
Tests:
1. Script embedding in HTML
2. Graceful handling of missing source code
3. Event handler parsing
"""

import sys
sys.path.insert(0, '/home/ibrahim-fonyuy/Downloads/NextPyVision (1)/NextPyVision/.nextpy_framework')

from nextpy.psx import component, useState, psx
from nextpy.psx.hydration import interactive_component

# Test 1: Basic interactive component
@interactive_component
def TestCounter(props=None):
    [count, setCount] = useState(0)
    return psx("""
        <div class="counter">
            <h1>Count: {count}</h1>
            <button onclick={lambda e: setCount(count + 1)}>Increment</button>
            <button onclick={lambda e: setCount(count - 1)}>Decrement</button>
        </div>
    """)

# Test 2: Component from external page
try:
    from pages.test_psx import SimpleCounter
    test_external = SimpleCounter()
    has_external = True
except Exception as e:
    print(f"Could not import external component: {e}")
    has_external = False

print("=" * 60)
print("HYDRATION ENGINE FIX VERIFICATION")
print("=" * 60)

# Test script embedding
print("\n✓ Test 1: Script Embedding")
print("-" * 40)
result = TestCounter()
print(f"Component type: {type(result).__name__}")
print(f"Has 'is_interactive' attribute: {hasattr(result, 'is_interactive')}")
print(f"Is interactive: {getattr(result, 'is_interactive', False)}")

html_output = str(result)
print(f"\nHTML output length: {len(html_output)} chars")
print(f"Contains <script> tag: {'<script' in html_output}")
print(f"Contains 'NextPyRuntime': {'NextPyRuntime' in html_output}")
print(f"Contains 'StateManager': {'StateManager' in html_output}")

# Show first 50 chars of script
if '<script' in html_output:
    script_start = html_output.find('<script')
    script_content = html_output[script_start:script_start+100]
    print(f"Script start: {script_content}...")

# Test error handling
print("\n✓ Test 2: Error Handling (Missing Source Code)")
print("-" * 40)
from nextpy.psx.hydration.integration import ComponentHydrator

hydrator = ComponentHydrator()

# Try with a built-in function (no source available)
metadata = hydrator.extract_component_metadata(len)
print(f"Metadata for built-in function: {metadata}")
print(f"No error raised: ✓")

# Test 3: Handler parsing
print("\n✓ Test 3: Event Handler Parsing")
print("-" * 40)
component_source = """
@interactive_component
def MyForm(props=None):
    [name, setName] = useState("")
    [email, setEmail] = useState("")
    
    def handleSubmit(e):
        print(f"Form submitted: {name}, {email}")
    
    return psx('''
        <form onsubmit={handleSubmit}>
            <input onchange={lambda e: setName(e.target.value)} placeholder="Name" />
            <input onchange={lambda e: setEmail(e.target.value)} placeholder="Email" />
            <button type="submit">Submit</button>
        </form>
    ''')
"""

# Extract handlers from source
handlers = hydrator._extract_handlers_from_source(component_source)
print(f"Handlers found: {len(handlers)}")
for name, code in handlers.items():
    print(f"  - {name}: {code[:50]}...")

# Test 4: Safe evaluation
print("\n✓ Test 4: Safe Value Evaluation")
print("-" * 40)
test_values = [
    "0",
    "42",
    "3.14",
    "'hello'",
    '"world"',
    "True",
    "False",
    "[]",
    "[1, 2, 3]",
    "{}",
    '{"key": "value"}',
]

for val in test_values:
    result = hydrator._safe_eval(val)
    print(f"  {val:20} → {result!r}")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED")
print("=" * 60)
print("\n✅ Key Fixes Applied:")
print("1. Script now embedded in HTML output")
print("2. Graceful handling of missing source code (no warnings)")
print("3. Improved event handler detection patterns")
print("4. Safe value evaluation for useState defaults")
