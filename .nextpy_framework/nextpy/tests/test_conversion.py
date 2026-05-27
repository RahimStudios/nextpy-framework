#!/usr/bin/env python3
"""
TEST: Direct conversion test
Test convert_handler_attributes_in_html directly
"""

import sys
sys.path.insert(0, '/home/ibrahim-fonyuy/Downloads/NextPyVision (1)/NextPyVision/.nextpy_framework')

from nextpy.psx.hydration.decorators import convert_handler_attributes_in_html

# Test HTML with various patterns
html = """
<div>
    <button onclick={handleIncrement}>Named handler</button>
    <button create_onclick={handleIncrement}>Create on handler</button>
    <button onclick={lambda e: setCount(count + 1)}>Lambda handler</button>
    <button create_onclick={lambda e: setCount(count - 1)}>Create lambda</button>
</div>
"""

handlers = {
    'handleIncrement': 'setCount(count + 1)',
    'lambda_handler_123': 'setCount(count + 1)',  # Simulate lambda
    'create_lambda_handler_456': 'setCount(count - 1)'  # Simulate create lambda
}

state_keys = ['count']

result = convert_handler_attributes_in_html(html, handlers, state_keys)

print("Original HTML:")
print(html)
print("\nConverted HTML:")
print(result)

# Check conversions
print("\nChecks:")
print("Contains data-handler-click:", 'data-handler-click' in result)
print("Contains data-handler for lambda:", 'lambda_handler' in result)
print("Contains data-handler for create:", 'create_lambda_handler' in result)