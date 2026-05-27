#!/usr/bin/env python3
"""Test the PSX runtime integration"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.nextpy_framework'))

from nextpy.psx.core.runtime import PSXRuntime
from nextpy.psx.core.ast_nodes import ElementNode

# Create a test context with interactive handlers
context = {'_interactive_handlers': {'handle_increment': True, 'handle_reset': True}}

# Create a test element node with events
element = ElementNode(
    tag='button',
    attributes={'class': 'btn'},
    events={'onClick': 'handle_increment'},
    children=['Increment']
)

# Create runtime and test
runtime = PSXRuntime(context)
html = runtime._render_element_node(element)

print("Generated HTML:")
print(html)
print("\nExpected: data-handler-click should be present")

if 'data-handler-click' in html:
    print("SUCCESS: Interactive component integration working!")
else:
    print("FAILED: data-handler-click not found")
