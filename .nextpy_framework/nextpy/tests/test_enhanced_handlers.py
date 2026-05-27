#!/usr/bin/env python3
"""
TEST: Enhanced Handler Support
Test create_on utilities and inline lambda handlers
"""

import sys
sys.path.insert(0, '/home/ibrahim-fonyuy/Downloads/NextPyVision (1)/NextPyVision/.nextpy_framework')

from nextpy.psx import psx, component, useState, create_onclick, create_onchange
from nextpy.psx.hydration import interactive_component


@interactive_component
def EnhancedTestComponent(props=None):
    [count, setCount] = useState(0)
    
    # create_on utilities
    handleIncrement = create_onclick(lambda e: setCount(count + 1))
    
    # Return HTML with patterns that convert_handler_attributes_in_html expects
    return """
        <div>
            <h1>Count: {count}</h1>
            <button create_onclick={handleIncrement}>Increment</button>
            <button onclick={lambda e: setCount(count - 1)}>Decrement</button>
        </div>
    """


print("=" * 60)
print("ENHANCED HANDLER SUPPORT TEST")
print("=" * 60)

# Render component
result = EnhancedTestComponent()

html = str(result)

print(f"\n✓ HTML generated: {len(html)} chars")

# Check for data-handler attributes
print(f"✓ Contains data-handler-click: {'data-handler-click' in html}")
print(f"✓ Contains data-handler-change: {'data-handler-change' in html}")

# Check for lambda handlers
print(f"✓ Contains lambda_handler: {'lambda_handler' in html}")
print(f"✓ Contains create_lambda_handler: {'create_lambda_handler' in html}")

# Count handlers
click_handlers = html.count('data-handler-click')
change_handlers = html.count('data-handler-change')
total_handlers = html.count('data-handler-')

print(f"\nHandler counts:")
print(f"  - click handlers: {click_handlers}")
print(f"  - change handlers: {change_handlers}")
print(f"  - total data-handler attributes: {total_handlers}")

# Check script section
if '<script' in html:
    script_start = html.find('<script')
    script_end = html.find('</script>', script_start) + len('</script>')
    script_section = html[script_start:script_end]
    
    print(f"\n✓ Script section: {len(script_section)} chars")
    print(f"✓ Contains lambda_handler: {'lambda_handler' in script_section}")
    print(f"✓ Contains create_lambda_handler: {'create_lambda_handler' in script_section}")
    
    # Show handler registrations
    lines = script_section.split('\n')
    handler_lines = [line for line in lines if 'registerHandler' in line or 'lambda_handler' in line or 'create_lambda_handler' in line]
    if handler_lines:
        print(f"\nHandler registrations found:")
        for line in handler_lines[:5]:  # Show first 5
            print(f"  {line.strip()}")

print("\n" + "=" * 60)
if click_handlers >= 2 and change_handlers >= 1 and 'lambda_handler' in html:
    print("✅ ENHANCED HANDLER TESTS PASSED")
else:
    print("❌ SOME TESTS FAILED")
print("=" * 60)